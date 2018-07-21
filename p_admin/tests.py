from django.test import TestCase
from django.db import models
from django.utils import timezone

class calendar(models.Model):
    cate=(
    ('1',u'正常上班'),
    ('2',u'假日休息'),
    ('3',u'节假日休息'),
    ('4',u'调班休息')
    )  
    code = models.CharField(max_length=40,verbose_name='日历编码')
    cdate = models.ManyToManyField('self',verbose_name='日期')
    category = models.CharField(max_length=10, verbose_name='状态')
    cdescription = models.TextField(null=True,blank=True,verbose_name='说明')      
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")

    def __str__(self):
        return '%s-%s(%s)' %(self.code,self.cdate,self.category)

    class Meta:
        verbose_name='<Admin>9.1.3日历设置'
        verbose_name_plural='<Admin>9.1.3日历设置'
        permissions = (("calendar_view", u"查看日历设置"),)

'''
class timetable(models.Model):
    cate=(
    ('1',u'工作时间'),
    ('2',u'加班时间'),
    ('3',u'中间休息')
    )  
    code = models.CharField(max_length=40,verbose_name='班表编码')
    starttime = models.TimeField(verbose_name='开始时间')
    endtime=models.TimeField(verbose_name='结束时间')
    category = models.CharField(max_length=10, verbose_name='状态')
    tdescription = models.TextField(null=True,blank=True,verbose_name='说明')      
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")

    def __str__(self):
        return '%s-%s(%s)' %(self.code,self.cdate,self.category)

    class Meta:
        verbose_name='<Admin>9.1.4班表设置'
        verbose_name_plural='<Admin>9.1.4班表设置'
        permissions = (("timetable_view", u"查看班表设置"),)

        '''