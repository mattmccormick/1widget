#!/usr/local/bin/python2.6
import os, sys
sys.path.append('/home/widget')
sys.path.append('/home/widget/twitter')
os.environ['DJANGO_SETTINGS_MODULE'] = 'twitter.settings'

from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User, Group
from twitter.control.models import Paypal, Digest, Feed

free = Group.objects.get(name='Free')
users = User.objects.filter(paypal__expiry_date=datetime.now())

for user in users:
    user.groups = [free]
    
    try:
        # inactivate all digests except the most recently added
        recent = Digest.objects.filter(user=user).order_by('-time_added')[0]
        old = Digest.objects.filter(user=user).exclude(id=recent.id)
        for digest in old:
            digest.delete()
        
        # for the remaining digest, remove all but five feeds
        extra_feeds = recent.feeds.all()[5:]
        for feed in extra_feeds:
            recent.feeds.remove(feed)
            
    except IndexError:
        pass # user does not have any digests   

print users