# -*- coding:utf-8 -*-
from django.apps import AppConfig
import os

#default_app_config = 'p_admin.apps.AppadminConfig'
'''
def get_current_app_name(file):
    return os.path.split(os.path.dirname(__file__))[-1]

class runtimeConfig(AppConfig):
    name = get_current_app_name(__file__)
    print(name)
    verbose_name = u"3.5.3运行工作流"
    
default_app_config = get_current_app_name(__file__) + '.__init__.runtimeConfig'
'''