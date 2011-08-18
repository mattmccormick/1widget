import logging, urllib, urllib2
from datetime import datetime, timedelta

from django.conf import settings
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from twitter.feeds.forms import RegisterForm, LoginForm
from twitter.control.models import Paypal, Digest, View
from twitter.control.GroupInfo import GroupInfo
from twitter.ctctwspylib.ConstantContact import ConstantContact

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/control/')
    
    f = urllib2.urlopen('http://www.1widget.com/feed/rcaGhNtSvdDnfOFyLI11.html')
    
    return render_to_response('base_index.html', {'demo': f.read()}, 
                              context_instance=RequestContext(request))        
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            #cc = ConstantContact()
            #cc.signup(email)
            user = authenticate(email=email, 
                                password=form.cleaned_data['password'])
            auth_login(request, user)
            request.session['signup'] = True
            return HttpResponseRedirect('/pricing')
    else:
        form = RegisterForm()
        
    return render_to_response('registration/register.html', {'form': form}, 
                              context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            auth_login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = LoginForm()
        
    return render_to_response('registration/login.html', {'form': form},
                              context_instance=RequestContext(request))
    
def default(request, page):
    groupinfo = None
    signup = False
    
    if page == 'pricing' and request.user.is_authenticated():
        if request.session.get('signup'):
            signup = True
            request.session['signup'] = False
            
        groupinfo = GroupInfo(request.user)
        
    return render_to_response(page + '.html', {'groupinfo': groupinfo,
                                               'signup': signup}, 
                              context_instance=RequestContext(request))
    
def get(request, id):
    try:
        digest = Digest.objects.get(digest_id=id)
    except:
        raise Http404
    
    today = datetime.today()
    try:
        view = View.objects.get(digest=digest, date=today)
    except:
        view = View(digest=digest)
        view.save()
        
    groupinfo = GroupInfo(digest.user)
    if view.views >= groupinfo.get_views_limit():
        response = '<p>Digest has been accessed too many times today.\
            The site owner can go to <a href="http://www.1widget.com">1widget.com</a>\
            to upgrade their 1widget package.</p>'
    else:
        view.views += 1
        view.save()
        
        file = "/home/widget/public_html/twitter/%s.html" % (id)
        f = open(file, 'r')
        response  = f.read()
        f.close()
        
    return HttpResponse(response, 'text/html') 

    
def paypal_ipn(request):
    postdata = urllib.urlencode(request.POST)
    resp = urllib.urlopen('https://www.paypal.com/cgi-bin/webscr', 
                          data='cmd=_notify-validate&' + postdata)
    
    out = resp.read()
    logging.basicConfig(filename='/home/widget/twitter/logs/ipn.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(out + ' ' + postdata)
    
    if out == 'VERIFIED' and request.POST.get('txn_type') == 'subscr_cancel':
        date_str = urllib.unquote_plus(request.POST.get('subscr_date'))
        sub_date = datetime.strptime(date_str, "%H:%M:%S %b %d, %Y %Z")
        
        n = datetime.now()
        
        if n.day < sub_date.day:    # expires this month
            expiry_date = datetime(n.year, n.month, sub_date.day)
        else:   # expires next month
            nextmonth = n + timedelta(days=30)
            expiry_date = datetime(nextmonth.year, nextmonth.month, sub_date.day)
            
        try:
            paypal = Paypal.objects.get(payer_id=request.POST.get('payer_id'),
                                    subscr_id=request.POST.get('subscr_id'))
         
            paypal.expiry_date = expiry_date.strftime("%Y-%m-%d")
            paypal.save()
            
            email_text = "Thank you for using 1widget.\
Your subscription cancellation has been received.\
Your account will be active until %s and then will be changed into a Free package.\
At that time, only your most recent digest with five feeds will be available.\n\n\
If you have any questions or feedback on our service, please reply to this email." % (paypal.expiry_date)

            send_mail('1widget: Cancel Subscription', email_text, 
                  'service@1widget.com', ['%s' % (request.user.email)])
        except:
            send_mail('Exception', request.POST, 
                  'service@1widget.com', ['service@1widget.com',])
            pass
                
    return HttpResponse(out)
