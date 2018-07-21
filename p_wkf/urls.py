from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth import logout, login
from p_wkf.forms import DefaultAppStartForm
from p_wkf.views import *


urlpatterns = [
    url(r'^$', index),
    url(r'^process/dot/(?P<id>.*)$',process_dot),
    url(r'^cron/$',cron),
]

urlpatterns += [
    url(r'^home/$', wkf),
    url(r'^otherswork/$',                 otherswork),
    url(r'^otherswork/instancehistory/$', instancehistory),
    url(r'^myrequests/$',                 myrequests),
    url(r'^myrequests/instancehistory/$', instancehistory),
    url(r'^mywork/$',                     mywork),
    url(r'^mywork/activate/(?P<id>.*)/$', activate),
    url(r'^mywork/complete/(?P<id>.*)/$', complete),
]

