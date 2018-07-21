from django.contrib import admin
from django.db.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from goflow.workflow.models import Transition, Process, Application, PushApplication, Activity, UserProfile


class TransitionInline(admin.StackedInline):
    model = Transition
    fieldsets = (
              (None, {'fields':(('input', 'output'), 'condition', 'precondition')}),
              )

#流程定义
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled', 'summary', 'priority')
    inlines = [
                   TransitionInline,
               ]
admin.site.register(Process, ProcessAdmin)

#过程应用
class ApplicationAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('url', 'documentation', 'test')
admin.site.register(Application, ApplicationAdmin)

#推送应用
class PushApplicationAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('url', 'documentation', 'test')
admin.site.register(PushApplication, PushApplicationAdmin)

#过程定义
class ActivityAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('title', 'description', 'kind', 'application', 
                    'join_mode', 'split_mode', 'autostart', 'autofinish', 'process')
    list_filter = ('process', 'kind')
    fieldsets = (
              (None, {'fields':(('kind', 'subflow'), ('title', 'process'), 'description')}),
              ('Push application', {'fields':(('push_application', 'pushapp_param'),)}),
              ('Application', {'fields':(('application', 'app_param'),)}),
              ('I/O modes', {'fields':(('join_mode', 'split_mode'),)}),
              ('Execution modes', {'fields':(('autostart', 'autofinish'),)}),
              ('Permission', {'fields':('roles',)}),
              )
admin.site.register(Activity, ActivityAdmin)

#过程转换
class TransitionAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('__str__', 'input', 'output', 'condition', 'description', 'process')
    list_filter = ('process',)
    fieldsets = (
              (None, {'fields':(
                                ('name', 'description'),
                                'process',
                                ('input', 'output'),
                                'condition', 'precondition'
                                )
                     }),
              )
admin.site.register(Transition, TransitionAdmin)

#用户消息
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'web_host', 'notified', 'last_notif', 'nb_wi_notif', 'notif_delay')
    list_filter = ('web_host', 'notified')
admin.site.register(UserProfile, UserProfileAdmin)

'''
#User界面加入UserProfile
admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1

class GoFlowUserAdmin(UserAdmin):
    inlines = [UserProfileInline]    
admin.site.register(User, GoFlowUserAdmin)
'''