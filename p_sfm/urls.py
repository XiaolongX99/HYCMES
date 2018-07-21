#p_sfm urls
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p_sfm import views

urlpatterns = [
    path('<str:mds>/',views.sfm,name='sfm'),
    path('qc/<str:mds>/',views.sfm,name='qc'),
    path('dispatch/<str:fun>/',views.dispatch,name='dispatch'),
    path('transfer/<str:fun>/',views.transfer,name='transfer'),


    
]