# -*- coding:utf-8 -*-
from django.contrib import admin
from django.conf.urls import include, url

from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.search import urls as wagtailsearch_urls
from p_cms import views

urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'home/', views.cms),
    url(r'', include(wagtail_urls)),
]