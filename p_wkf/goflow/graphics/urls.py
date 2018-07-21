from django.conf.urls import url

from goflow.graphics import views

urlpatterns = [
    url(r'^(?P<id>.*)/save/$', views.graph_save),
    url(r'^(?P<id>.*)/$', views.graph, {'template':'goflow/graphics/graph.html'}),
]
