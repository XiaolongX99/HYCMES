# -*- coding:utf-8 -*-
from django.contrib import admin
from django.db import models
from django import forms
from django.contrib.auth.models import User,Group,UserManager 
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


#组织部门
class department(models.Model):
    cate=(
    ('0',u'公司集团'),
    ('1',u'工厂'),
    ('2',u'事业部'),
    ('3',u'职能部门'),
    ('4',u'作业单位'),
    ('P',u'生产线'),
    ('C',u'Cell')    
    )    
    code=models.CharField(max_length=40,primary_key=True,verbose_name='部门代码')
    name=models.CharField(max_length=40,unique=True,verbose_name='部门名称')
    parent=models.ForeignKey('self',related_name='parents',on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name='上级部门')
    responsibility=models.ForeignKey(User,related_name='managers',on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name='权责主管')
    category=models.CharField(max_length=40,choices=cate,verbose_name='部门类别')
    createdate=models.DateField(default=timezone.now,verbose_name='创建时间')
    jn=models.ManyToManyField('organization',blank=True,verbose_name='直属人员')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name='1301部门组织'
        verbose_name_plural='1301部门组织'
        ordering = ['category','code']

#组织人员
class organization(models.Model):
    tit=(
    ('1',u'职员'),
    ('2',u'作业员'),
    ('3',u'工程师'),
    ('4',u'组长'),
    ('5',u'主管'),
    ('6',u'经理'),
    ('7',u'总监'),
    ('8',u'副总经理'),
    ('9',u'总经理')
    )    
    jn=models.CharField(max_length=10,primary_key=True,verbose_name='工号')
    name=models.CharField(max_length=20,verbose_name='姓名')
    dep=models.ForeignKey('department',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='deporganization',verbose_name='所属部门')
    ondate=models.DateField(default=timezone.now,null=True,blank=True,verbose_name='到职日期')    
    title=models.CharField(max_length=40,choices=tit,null=True,blank=True,verbose_name='职务')
    states=models.BooleanField(default=1,verbose_name='在职状态')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s(%s)' %(self.name,self.jn)

    class Meta:
        verbose_name = '1302组织人员'
        verbose_name_plural = '1302组织人员'
        ordering = ['dep','jn']

#系统模组
class module(models.Model):
    lev=(
    (0,u'系统'),
    (1,u'子系统'),
    (2,u'模组'),
    (3,u'次级模组'),
    (4,u'功能'),
    (5,u'次级功能'),
    (6,u'对像'),
    )  
    code=models.CharField(max_length=40,primary_key=True,verbose_name='模组代码')
    name=models.CharField(max_length=40,unique=True,verbose_name='模组名称')
    parent=models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name='上级模组')
    url=models.CharField(max_length=120,null=True,blank=True,verbose_name='模组路径')
    icon=models.CharField(max_length=120,null=True,blank=True,verbose_name='图标')
    level=models.SmallIntegerField(default=2,choices=lev,verbose_name='层级')
    group=models.ManyToManyField(Group, null=True,blank=True,verbose_name='模组分配给角色')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '1303系统模组'
        verbose_name_plural = '1303系统模组'
        ordering = ['code'] 


#个人设置 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,verbose_name='用户')
    avatar = models.ImageField(upload_to='images',null=True,blank=True,verbose_name='头像')
    telphone = models.CharField(max_length=40, null=True,blank=True,verbose_name='手机')   
    onwer=models.ForeignKey('department',on_delete=models.DO_NOTHING,related_name='onwers',null=True,blank=True,verbose_name='直属部门')
    department=models.ManyToManyField('department',related_name='deps',null=True, blank=True,verbose_name='管理部门')
    module=models.ManyToManyField('module',related_name='mds',null=True, blank=True,verbose_name='管理模组')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name='1304个人设置'
        verbose_name_plural='1304个人设置'

    def save(self, **kwargs):
        models.Model.save(self,  **kwargs)

#日期轴
class axisdate(models.Model):
    AXD=models.DateField(primary_key=True,verbose_name='日期')
    WK=models.IntegerField(verbose_name='星期')
    MON=models.IntegerField(verbose_name='月份')
    YEA=models.IntegerField(verbose_name='年份')

    def __str__(self):
        return '%s(%s)'% (self.AXD.strftime("%Y-%m-%d"),self.WK)

    class Meta:
        verbose_name='1305日期轴'
        verbose_name_plural='1305日期轴'

#时间轴
class axistime(models.Model):
    AXT=models.TimeField(primary_key=True,verbose_name='时间')
    TT=models.CharField(max_length=20,null=True,blank=True,verbose_name='时间类型')

    def __str__(self):
        return self.AXT.strftime("%H:%M")

    class Meta:
        verbose_name='1306时间轴'
        verbose_name_plural='1306时间轴'

#日历
class calendar(models.Model):
    code = models.CharField(max_length=40,primary_key=True,verbose_name='日历编码',help_text='设置前后1年工作日历。' )    
    cdescription = models.TextField(null=True,blank=True,verbose_name='说明',help_text='筛选出各节假日休息日，其它日期默认为工作日。' )      
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    cdate = models.ManyToManyField('axisdate',verbose_name='日期')

    def __str__(self):
        return '%s-%s' %(self.code,self.cdescription)

    class Meta:
        verbose_name='1307日历设置'
        verbose_name_plural='1307日历设置'

#班表
class timetable(models.Model):
    code = models.CharField(max_length=40,primary_key=True,verbose_name='班表编码',help_text='依据各部门上下班时间不同设置。')    
    tdescription = models.TextField(null=True,blank=True,verbose_name='说明',help_text='筛选出各段工作时间，其余时间默认为休息状态。')      
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    ctime = models.ManyToManyField('axistime',verbose_name='时间')

    def __str__(self):
        return '%s(%s)' %(self.code,self.tdescription)

    class Meta:
        verbose_name='1308班表设置'
        verbose_name_plural='1308班表设置'    


class ProjectUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey('module', on_delete=models.CASCADE)

class ProjectGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey('module', on_delete=models.CASCADE)