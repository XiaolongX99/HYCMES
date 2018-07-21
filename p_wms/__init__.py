# -*- coding:utf-8 -*-
from django.apps import AppConfig
import os

#default_app_config = 'p_admin.apps.AppadminConfig'

def get_current_app_name(file):
    return os.path.split(os.path.dirname(__file__))[-1]

class p_wmsConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u"06.仓储管理"
    
default_app_config = get_current_app_name(__file__) + '.__init__.p_wmsConfig'