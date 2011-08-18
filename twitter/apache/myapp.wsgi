import os, sys
sys.stdout = sys.stderr
sys.path.append('/home/widget')  # needs to be the parent of the project directory
sys.path.append('/home/widget/twitter')
os.environ['DJANGO_SETTINGS_MODULE'] = 'twitter.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/widget/.python-eggs'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
