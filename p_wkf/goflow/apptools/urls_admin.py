from django.conf.urls import url

from goflow.apptools.views import image_update, app_env, test_start

urlpatterns = [
    url(r'^icon/image_update/$', image_update),
    url(r'^application/testenv/(?P<action>create|remove)/(?P<id>.*)/$', app_env),
    url(r'^application/teststart/(?P<id>.*)/$', test_start),
]
