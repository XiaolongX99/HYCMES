from django.conf.urls import url

from goflow.apptools import forms
from goflow.apptools.views import *

urlpatterns = [
    url(r'^start/(?P<app_label>.*)/(?P<model_name>.*)/$', start_application),
    url(r'^start_proto/(?P<process_name>.*)/$', start_application, {'form_class':forms.DefaultAppStartForm, 'template':'goflow/start_proto.html'}),
    url(r'^view_application/(?P<id>\d+)/$', view_application),
    url(r'^choice_application/(?P<id>\d+)/$', choice_application),
    url(r'^sendmail/$', sendmail),
]
