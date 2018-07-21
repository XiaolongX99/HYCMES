
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p_cim import views

urlpatterns = [
    path('<str:mds>/',views.cim,name='cim'),
    
]