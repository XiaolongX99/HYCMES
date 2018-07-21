# -*- coding:utf-8 -*-
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p_opm import views

urlpatterns = [
    path('<str:mds>/',views.opm,name='opm'),
    
]