# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group,User
from p_admin.models import department,module,Profile,organization,calendar,timetable
from p_wkf.models import UserProfile
from guardian.admin import GuardedModelAdmin

'''
# Register your models here.
class Myadmin(GuardedModelAdmin):
    """admin界面的定义"""
    #list_display = ['proid','proname','prostarttime','prorelease','proreltime','proplantime']
    filter_horizontal = ['group']
admin.site.register(module, Myadmin)
'''

#组织部门
@admin.register(department)
class departmentAdmin(admin.ModelAdmin):
    list_filter = ["category"]
    search_fields = ["code", "name"]
    list_display =['name','code','responsibility','parent']
    filter_horizontal=('jn',)

#组织人员    
@admin.register(organization)
class organizationAdmin(admin.ModelAdmin):
    list_filter = ["dep",'title']
    search_fields = ["jn", "name",'ondate']
    list_display =['name','jn','title','dep','ondate']


#系统模组
@admin.register(module)
class moduleAdmin(admin.ModelAdmin):
    list_filter = ['level',"parent"]
    search_fields = ['name','code']
    list_display =['name','code','parent','url','level']
    filter_horizontal=('group',)


#个人设置
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ["onwer"]
    search_fields = ['user','telphone']
    list_display =['user','telphone']
    filter_horizontal=('department','module',)

#个人消息 from workflow
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1

#个人资讯
admin.site.unregister(User)
class ProfileInline(admin.StackedInline):
    model = Profile    
    max_num = 1
    can_delete = False
    filter_horizontal=('department','module',)

#定制用户界面
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,UserProfileInline]
admin.site.register(User, CustomUserAdmin)


#工作日历
@admin.register(calendar)
class calendarAdmin(admin.ModelAdmin):
    search_fields = ["code"]
    list_display =['code','cdescription']
    filter_horizontal=('cdate',)


#工作班表
@admin.register(timetable)
class timetableAdmin(admin.ModelAdmin):
    search_fields = ["code"]
    list_display =['code','tdescription']
    filter_horizontal=('ctime',)
