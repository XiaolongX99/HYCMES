# -*- coding:utf-8 -*-
from django.apps import AppConfig
import os

#default_app_config = 'p_admin.apps.AppadminConfig'

def get_current_app_name(file):
    return os.path.split(os.path.dirname(__file__))[-1]

class p_scmConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u"05.供应链"
    
default_app_config = get_current_app_name(__file__) + '.__init__.p_scmConfig'