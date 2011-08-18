from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','twitter.feeds.views.index', name='index'),
    url(r'^register$','twitter.feeds.views.register', name='register'),
    url(r'^login$','twitter.feeds.views.login', name='login'),
    url(r'^logout$','django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^reset$', 'django.contrib.auth.views.password_reset', name='reset'),
    url(r'^reset-confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset-complete$', 'django.contrib.auth.views.password_reset_done', name='reset-complete'),
    url(r'^reset-done$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^(?P<page>pricing)$', 'twitter.feeds.views.default', name='pricing'),
    url(r'^(?P<page>terms)$', 'twitter.feeds.views.default', name='terms'),
    url(r'^(?P<page>privacy)$', 'twitter.feeds.views.default', name='privacy'),
    url(r'^(?P<page>faq)$', 'twitter.feeds.views.default', name='faq'),
    url(r'^paypal-ipn$', 'twitter.feeds.views.paypal_ipn'),
    url(r'^feed/(?P<id>[a-zA-Z\d]+)\.html$', 'twitter.feeds.views.get'),
)

urlpatterns += patterns('',
    (r'^control/', include('twitter.control.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^(?P<page>\w+)$', 'twitter.feeds.views.default', name='page'),
    url(r'^twitter/', include('twitter_app.urls')),
)

