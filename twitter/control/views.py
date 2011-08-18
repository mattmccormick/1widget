import urllib

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import Group
from twitter.control.models import Digest, DigestForm, Feed, FeedForm, Rss, RssForm, Template, TemplateForm, TemplateFormBasic, Paypal, Oauth
from twitter.control.GroupInfo import GroupInfo
from twitter.ctctwspylib.ConstantContact import ConstantContact

@login_required()
def upgrade(request):
    paypal_pdt = 'SET_PAYPAL'
    paypal_pdt_test = 'SET_PAYPAL'

    data = {'cmd': '_notify-synch',
            'tx': str(request.GET.get('tx')),
            'at': paypal_pdt
            }

    postdata = urllib.urlencode(data)

    resp = urllib.urlopen('https://www.paypal.com/cgi-bin/webscr',
                          data=postdata)

    paypal_info = resp.read()
    params = paypal_info.splitlines()

    send_mail('Account Upgraded', '%s%s' % (request.user.id, paypal_info),
              'noreply@1widget.com',['mattmccor@gmail.com',])

    if params[0] == 'SUCCESS':
        user = request.user
        user.groups = [get_group(str(request.GET.get('amt')))]

        payer_id = ''
        subscr_id = ''
        for line in params:
            vals = line.split('=')
            if vals[0] == 'payer_id':
                payer_id = vals[1]
            if vals[0] == 'subscr_id':
                subscr_id = vals[1]

        paypal = Paypal(user=user, subscr_id=subscr_id, payer_id=payer_id)
        paypal.save()

        #cc = ConstantContact()
        #cc.paid(user.email)

        return HttpResponseRedirect('/control/upgrade_success')
    else:
        return HttpResponseRedirect('/control/upgrade_failure')

@login_required()
def upgrade_success(request):
    return render_to_response('control/upgrade.html', {},
                                 context_instance=RequestContext(request))

@login_required
def upgrade_failure(request):
    return render_to_response('control/upgrade_failure.html', {},
                              context_instance=RequestContext(request))

@login_required()
def unsubscribe(request):
    return render_to_response('control/unsubscribe.html', {},
                              context_instance=RequestContext(request))

@login_required()
def index(request):
    digests = Digest.objects.filter(user=request.user)
    groupinfo = GroupInfo(request.user)
    return render_to_response('control/index.html', {'digests': digests,
                                                     'groupinfo': groupinfo},
                              context_instance=RequestContext(request))

@login_required()
def new(request):
    message = ''
    groupinfo = GroupInfo(request.user)
    form = DigestForm()
    form.fields['template'].choices = templates_as_choices(request)

    if groupinfo.get_digests_limit() == Digest.objects.filter(user=request.user).count():
        message = 'You have reached your Digest limit of %i. \
            Please remove a Digest or <a href="/pricing">upgrade your package</a>\
            to add more.' % (groupinfo.get_digests_limit())

    elif request.method == 'POST':
        form = DigestForm(request.POST)
        if form.is_valid():
            digest = form.save(commit=False)
            digest.user = request.user
            digest.save()
            return HttpResponseRedirect(digest.get_feeds_url())

    return render_to_response('control/digest.html', {'form': form,
                                                      'message': message},
                              context_instance=RequestContext(request))

@login_required()
def edit(request, id):
    digest = get_object(request, Digest, id)
    if request.method == 'POST':
        form = DigestForm(request.POST, instance=digest)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/control/')
    else:
        form = DigestForm(instance=digest,initial={'template': digest.template.id})
        form.fields['template'].choices = templates_as_choices(request)

    return render_to_response('control/digest-edit.html', {'form': form},
                              context_instance=RequestContext(request))

@login_required()
def code(request, id):
    digest = get_object(request, Digest, id)
    return render_to_response('control/digest-code.html', {'digest': digest},
                              context_instance=RequestContext(request))

@login_required()
def delete(request, id):
    digest = get_object(request, Digest, id)
    if request.method == 'POST':
        digest.delete()
        return HttpResponseRedirect('/control/')

    return render_to_response('control/digest-delete.html', {'digest': digest},
                              context_instance=RequestContext(request))

@permission_required('control.add_template', login_url='/control/package-template')
def templates(request):
    templates = Template.objects.filter(user=request.user).order_by('name')
    return render_to_response('control/templates.html', { 'templates': templates },
                              context_instance=RequestContext(request))

@permission_required('control.add_template', login_url='/control/package-template')
def template_new(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)

        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return HttpResponseRedirect('/control/templates')
    else:
        form = TemplateForm()

    return render_to_response('control/template.html', {'form': form},
                              context_instance=RequestContext(request))

@permission_required('control.change_template', login_url='/control/package-template')
def template_edit(request, template_id):
    template = get_object(request, Template, id=template_id)

    if request.method == 'POST':
        form = TemplateForm(request.POST, instance=template)

        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return HttpResponseRedirect('/control/templates')
    else:
        form = TemplateForm(instance=template)

    return render_to_response('control/template.html', {'form': form},
                              context_instance=RequestContext(request))

@login_required()
def package_template(request):
    return render_to_response('control/package-template.html',{},
                              context_instance=RequestContext(request))

@login_required()
def feeds(request, id):
    digest = get_object(request, Digest, id)
    form_twitter = FeedForm();
    form_rss = RssForm()
    total_feeds = digest.feeds.all().count() + digest.rss.all().count()
    groupinfo = GroupInfo(request.user)
    message = ''
    return_url = '/control/%i/feeds' % digest.id

    if request.method == 'POST':
        if total_feeds == groupinfo.get_feeds_limit():
            message = 'You are at the Feed limit for this digest.\
                Remove a feed or <a href="/pricing">upgrade your package</a>\
                to add more.'

        elif request.POST.get('username'):    # user submitted Twitter form
            if twitter_add(request.POST, digest):
                return HttpResponseRedirect(return_url)
            else:
                form_twitter = FeedForm(request.POST)

        elif request.POST.get('url'):   # user submitted RSS form
            try:
                rss = Rss.objects.get(url=request.POST.get('url'))
                digest.rss.add(rss)
                digest.save()
                return HttpResponseRedirect(return_url)
            except:
                form_rss = RssForm(request.POST)
                if form_rss.is_valid():
                    rss = form_rss.save()
                    digest.rss.add(rss)
                    digest.save()
                    return HttpResponseRedirect(return_url)

    return render_to_response('control/feed.html', {'digest': digest,
                                                    'form_twitter': form_twitter,
                                                    'form_rss': form_rss,
                                                    'total': total_feeds,
                                                    'groupinfo': groupinfo,
                                                    'message': message},
                              context_instance=RequestContext(request))

def twitter_add(post, digest):
    result = False
    try:
        feed = Feed.objects.get(username=post.get('username'))
        digest.feeds.add(feed)
        digest.save()
        result = True
    except:
        form_twitter = FeedForm(post)
        if form_twitter.is_valid():
            feed = form_twitter.save()
            digest.feeds.add(feed)
            digest.save()
            result = True

    return result

@login_required()
def twitter(request):
    return render_to_response('control/twitter.html', {},
                              context_instance=RequestContext(request))

@login_required()
def feed_delete(request, id):
    digest = get_object(request, Digest, id)
    if digest.user == request.user:
        feed = digest.feeds.get(id=request.POST.get('id'))
        digest.feeds.remove(feed)
        digest.save()

    return HttpResponseRedirect(digest.get_feeds_url())

@login_required()
def rss_delete(request, id):
    digest = get_object(request, Digest, id)
    if digest.user == request.user:
        rss = digest.rss.get(id=request.POST.get('id'))
        digest.rss.remove(rss)
        digest.save()

    return HttpResponseRedirect(digest.get_feeds_url())

def get_object(request, type, id):
    object = get_object_or_404(type, id=id)
    if object.user != request.user:
        raise Http404

    return object

def templates_as_choices(request):
    templates = []
    default = []
    user = []
    for template in Template.objects.filter(default=1).order_by('name'):
        default.append([template.id, template.name])

    for template in Template.objects.filter(user=request.user).order_by('name'):
        user.append([template.id, template.name])

    templates.append(['Default Templates', default])

    if user:
        templates.append(['User Templates', user])

    return templates

def get_group(payment):
    if payment == '10.00':
        name = 'Small'
    elif payment == '40.00':
        name = 'Multi'
    elif payment == '150.00':
        name = 'Premium'
    else:
        name = 'Free'

    return Group.objects.get(name=name)
