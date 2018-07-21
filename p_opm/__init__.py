# -*- coding:utf-8 -*-
from django.apps import AppConfig
import os

def get_current_app_name(file):
    return os.path.split(os.path.dirname(__file__))[-1]

class p_opmConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u"03.运作绩效"
    
default_app_config = get_current_app_name(__file__) + '.__init__.p_opmConfig'