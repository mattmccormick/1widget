import random, string, array, urllib, urllib2, subprocess, os
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from twitter.control.MultiReplace import MultiReplace

class Paypal(models.Model):
    user = models.ForeignKey(User, unique=True)
    payer_id = models.CharField(max_length=13)
    subscr_id = models.CharField(max_length=19, unique=True)
    expiry_date = models.DateField(null=True)
     
    def __unicode__(self):
        return self.subscr_id
    

class Oauth(models.Model):
    user = models.ForeignKey(User, unique=True)
    token = models.CharField(max_length=255)
    token_secret = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.token
    

class Feed(models.Model):
    username = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        ordering = ['username']
        

class Rss(models.Model):
    url = models.URLField(unique=True)
    
    def __unicode__(self):
        return self.url
    
    def save(self):
        super(Rss, self).save()
        strid = str(self.id)
        outfile = '/home/widget/twitter/sources/rss/%s.rss' % (strid)
        urllib.urlretrieve(self.url, outfile)
        os.chmod(outfile, 0666)
        
        
class Template(models.Model):
    name = models.CharField('Template Name', max_length=255)
    default = models.BooleanField(default=0)
    user = models.ForeignKey(User)
    html = models.TextField()
    tpl = models.CharField(max_length=255)
    time_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/control/template/%i' % self.id
    
    def save(self):
        if self.default:
            raise Exception
        
        super(Template, self).save()
        if self.tpl == '':
            self.tpl = str(self.id) + '.tpl'
            super(Template, self).save()
            
        r = MultiReplace({'{': '{ldelim}', '}': '{rdelim}'})
        outhtml = r.replace(self.html)
        
        try:
            stylepos = outhtml.index('</style>')
            pos = stylepos + '</style>'.__len__()
        except ValueError:
            pos = 0
    
        outfile = '/home/widget/smarty/templates/' + self.tpl
        f = open(outfile, 'w')
        f.write(outhtml[0:pos] + '<div id="widget">{section name=i loop=$feeds}' 
                + outhtml[pos + 1:] + '{/section}</div>')
        f.close()
        os.chmod(outfile, 0666)
    
    class Meta:
        ordering = ['name']
    
    
class Digest(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    items = models.PositiveIntegerField('Number of items to display')
    keywords = models.CharField(max_length=255, null=True, blank=True,
                                help_text='<br />If you enter keywords, only feeds matching the keywords will be shown.\
                                Keywords will be taken as a phrase.\
                                If you want to match multiple keywords, separate with OR.\
                                eg. Super Bowl OR NFL<br /><br />\
                                Leave this field blank if you want all feeds to show.')
    digest_id = models.CharField(max_length=20, unique=True)
    time_added = models.DateTimeField(auto_now_add=True)
    feeds = models.ManyToManyField(Feed)
    rss = models.ManyToManyField(Rss)
    template = models.ForeignKey(Template, default=1)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    def delete(self):
        try:
            os.remove('/home/widget/public_html/twitter/%s.html' % self.digest_id)
        except OSError:
            pass
        
        super(Digest, self).delete()
    
    def save(self):
        super(Digest, self).save()
        strid = str(self.id)
        if self.digest_id == '':
            self.digest_id = array.array('c', random.sample(string.ascii_letters, 20 - len(strid))).tostring() + strid
            super(Digest, self).save()
        self.update_output()
    
    def update_output(self):
        subprocess.call(['php','/home/widget/action/digest.php', str(self.id)])
        
    def get_feeds_url(self):
        return '/control/%i/feeds' % self.id
    
    def get_digest_url(self):
        return 'http://www.1widget.com/feed/%s.html' % self.digest_id

    
class View(models.Model):
    digest = models.ForeignKey(Digest)
    date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('digest','date')

    
class DigestForm(ModelForm):
    class Meta:
        model = Digest
        fields = ['name','items','keywords','template']
        
        
class TemplateFormBasic(ModelForm):        
    class Meta:
        model = Digest
        fields = ['template']
        
        
class TemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['html'].widget.attrs['class'] = 'ckeditor'
        
    def clean_html(self):
        r = MultiReplace({'<?': '&lt;?', '<%=': '&lt;%='})
        return r.replace(self.cleaned_data['html'].strip())        
                                 
    class Meta:
        model = Template
        fields = ['name','html']
        
        
class FeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ['username']
        
    def clean_username(self):
        name = self.cleaned_data['username'].strip()
        
        filename = name + '.json'
        outfile = '/home/widget/twitter/sources/' + filename
        try:
            #TODO: check rate limits before call to twitter
            filehandle = urllib2.urlopen('http://twitter.com/statuses/user_timeline/' + filename)
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise forms.ValidationError('This user\'s Tweets are not public')
            elif e.code == 404:
                raise forms.ValidationError('Twitter Username does not exist')
            else:
                raise forms.ValidationError('There was an error getting this user\'s Tweets. Check that the username is valid. If it is valid, Twitter may just be down at the moment. Please try again in a few minutes')

        json_str = filehandle.read()
        
        f = open(outfile, 'w')
        f.write(json_str)
        f.close()
        os.chmod(outfile, 0666)
        
        return name
    

class RssForm(ModelForm):
    class Meta:
        model = Rss
        fields = ['url']