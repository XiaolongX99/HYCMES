from django.contrib import admin
from django.db.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from p_wkf.models import Image, Icon, ImageButton,Transition, Process, Application, PushApplication, Activity, UserProfile,ProcessInstance, WorkItem, Event



class ImageAdmin(admin.ModelAdmin):
    list_display = ('category', 'graphic', 'file', 'url')
    list_filter = ('category',)
admin.site.register(Image, ImageAdmin)

class IconAdmin(admin.ModelAdmin):
    list_display = ('category', 'graphic', 'url')
    list_filter = ('category',)
admin.site.register(Icon, IconAdmin)

class ImageButtonAdmin(admin.ModelAdmin):
    raw_id_fields = ('icon',)
    list_display = ('action', 'label', 'graphic')
admin.site.register(ImageButton, ImageButtonAdmin)



#workflow
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



class ProcessInstanceAdmin(admin.ModelAdmin):
    date_hierarchy = 'creationTime'
    list_display = ('title', 'process', 'user', 'creationTime', 'status', 'workitems_list')
    list_filter = ('process', 'status', 'user')
    fieldsets = (
              (None, {'fields':(
                                'title', 'process', 'user',
                                ('status', 'old_status'),
                                'condition',
                                ('object_id', 'content_type'))
                     }),
              )
admin.site.register(ProcessInstance, ProcessInstanceAdmin)

#工作项目
class WorkItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'user', 'instance', 'activity', 'status', 'events_list')
    list_filter = ('status', 'user', 'activity',)
    fieldsets = (
              (None, {'fields':(
                                ('instance', 'activity'),
                                'user',
                                'workitem_from',
                                ('status', 'blocked', 'priority'),
                                'push_roles', 'pull_roles')
                     }),
              )
admin.site.register(WorkItem, WorkItemAdmin)


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'name', 'workitem')
admin.site.register(Event, EventAdmin)