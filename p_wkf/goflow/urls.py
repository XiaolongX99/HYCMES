from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth import logout, login
from goflow.apptools.forms import DefaultAppStartForm
from goflow.apptools.views import start_application, default_app
from goflow.runtime.views import *
from goflow.workflow.views import process_dot, index, cron

urlpatterns = [
    url(r'^.*/logout/$', logout,name='logout'),
    url(r'^.*/accounts/login/$', login, {'template_name':'goflow/login.html'}),
    url(r'^apptools/', include('goflow.apptools.urls')),
    url(r'^graph/', include('goflow.graphics.urls')),
]

urlpatterns += [
    url(r'^$', index),
    url(r'^process/dot/(?P<id>.*)$',process_dot),
    url(r'^cron/$',cron),
]

urlpatterns += [
    url(r'^default_app/(?P<id>.*)/$', default_app),
    url(r'^start/(?P<app_label>.*)/(?P<model_name>.*)/$', start_application),
    url(r'^start_proto/(?P<process_name>.*)/$', start_application,
        {'form_class':DefaultAppStartForm,
         'redirect':'../../',
         'template':'goflow/start_proto.html'}),
]

urlpatterns += [
    url(r'^otherswork/$',                 otherswork),
    url(r'^otherswork/instancehistory/$', instancehistory),
    url(r'^myrequests/$',                 myrequests),
    url(r'^myrequests/instancehistory/$', instancehistory),
    url(r'^mywork/$',                     mywork),
    url(r'^mywork/activate/(?P<id>.*)/$', activate),
    url(r'^mywork/complete/(?P<id>.*)/$', complete),
]
