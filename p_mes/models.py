# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from p_admin.models import department
from django.db.models import When, F, Q

#mes models
class deptarget(models.Model):
    tcd=(
    ('ACR',u'生产力'),
    ('EFY',u'效率'),
    ('URT',u'利用率'),
    ('FCY',u'直通率'),
    ('UPPH',u'人均小时产出'),
    ('FG',u'完工数'),
    ('PPM',u'百万缺陷率')    
    )    
    dep=models.ForeignKey(department,on_delete=models.CASCADE,limit_choices_to=Q(category='P') | Q(category='C'),verbose_name='部门')
    tcode=models.CharField(max_length=40,verbose_name='目标项目')
    tvalue=models.DecimalField(max_digits=12,decimal_places=2,default=1,verbose_name='目标值')
    tucl=models.DecimalField(max_digits=12,decimal_places=2,default=1.25,verbose_name='上限')
    tlcl=models.DecimalField(max_digits=12,decimal_places=2,default=0.75,verbose_name='下限')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")

    def __str__(self):
        return self.tcode

    class Meta:
        verbose_name = '001看板目标'
        verbose_name_plural = '001看板目标'
        ordering = ['dep','tcode']
        unique_together = ('dep','tcode',)


class  SumReport(models.Model):
    WorkingDate = models.DateField(auto_now=False, auto_now_add=False,verbose_name='工作日期')
    PL = models.CharField(max_length=80,null=True,verbose_name='部门')
    Cell = models.CharField(max_length=80,null=True,verbose_name='Cell')
    Operation = models.CharField(max_length=80,null=True,verbose_name='工站')
    MPSQty = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='计划完工数')
    CompleteQty = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='实际完工数')
    PQ = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='人数')
    OutputHR = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='完工工时')
    ATH = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='出勤工时')
    NWK = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='无效工时')
    URT = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='工时利用率')
    Efficiency = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='作业效率')
    Productivity = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='综合生产力')
    AchievingRate = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='交期达率')
    StandardProductQty = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='标准完工数')
    Members = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='计划人数')
    WorkingHours = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='计划工时')
    UPPH = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='人均小时产出')
    Item = models.TextField(null=True,verbose_name='无效项目')
    PPM = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='百万分之')
    FCY = models.DecimalField(max_digits=12, decimal_places=4,null=True,verbose_name='直通率')
    
    class Meta:
        verbose_name='002MES报表'
        verbose_name_plural='002MES报表'
 
