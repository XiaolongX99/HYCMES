#p_sfm urls
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p_erp import views

urlpatterns = [
    path('<str:mds>/',views.erp,name='erp'),
    
]