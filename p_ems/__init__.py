from django.apps import AppConfig
import os

def get_current_app_name(file):
    return os.path.split(os.path.dirname(__file__))[-1]

class p_emsConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u"07设备维护"
    
default_app_config = get_current_app_name(__file__) + '.__init__.p_emsConfig'