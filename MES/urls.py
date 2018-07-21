#MES URL Configuration
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', include('p_admin.urls')),    
    path('mes/', include('p_mes.urls')),
    path('sfm/', include('p_sfm.urls')),
    path('pdm/', include('p_pdm.urls')),
    path('opm/', include('p_opm.urls')),
    path('aps/', include('p_aps.urls')),
    path('scm/', include('p_scm.urls')),
    path('wms/', include('p_wms.urls')),
    path('ems/', include('p_ems.urls')),
    path('crm/', include('p_crm.urls')),    
    path('erp/', include('p_erp.urls')),
    path('cim/', include('p_cim.urls')), 
    path('cms/', include('p_cms.urls')), 
    path('wkf/', include('p_wkf.urls')),  
    path('admin/',admin.site.urls), 

]

