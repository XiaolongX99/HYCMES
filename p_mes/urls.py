#p_sfm urls
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p_mes import views

urlpatterns = [
	path('dashboard/',views.dashboard),
	#path('dashboard/<str:mds>',views.dashboardetail),
    
]