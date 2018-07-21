# -*- coding:utf-8 -*-
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p_admin import views

urlpatterns = [
    path('',views.index),    
    path('login/', views.login),
    path('logout/', views.logout),
    path('reminder/', views.reminder),
    path('register/', views.register),
    path('lock/', views.lock),
    path('unlock/', views.unlock), 
    path('profile/<str:mds>/', views.profile),   
]