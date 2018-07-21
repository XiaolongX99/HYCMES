
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p_aps import views

urlpatterns = [
    path('<str:mds>/',views.aps,name='aps'),
    
]