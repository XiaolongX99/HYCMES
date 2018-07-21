from django.conf.urls import url
from django.conf.urls.defaults import *
from goflow.graphics import views as goflow_graphics_views
urlpatterns = [
    url(r'^processimage/(?P<process_id>.*)/pos_activity/$', goflow_graphics_views.pos_activity),
]
