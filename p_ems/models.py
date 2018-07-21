# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from p_admin.models import department
from django.contrib.auth.models import User
from p_pdm.models import operation
from django.db.models import When, F, Q

"""
from django.conf import settings
def upload_to(instance, fielname):
    return '/'.join([settings.MEDIA_ROOT, 'TPM', filename])
"""

class assets(models.Model):
    scode=models.CharField(max_length=40,primary_key=True,verbose_name='资产编码')
    sname=models.CharField(max_length=80,verbose_name='设备名称')
    sspec=models.CharField(max_length=40,null=True,blank=True,verbose_name='设备规格')
    category=models.CharField(max_length=40,null=True,blank=True,verbose_name='类型')
    parent=models.CharField(max_length=40,null=True,blank=True,verbose_name='主件编码')
    assets=models.CharField(max_length=40,null=True,blank=True,verbose_name='资产类别')
    supply=models.CharField(max_length=40,null=True,blank=True,verbose_name='设备厂家')
    eqty=models.SmallIntegerField(default=1,verbose_name='数量')
    durable=models.SmallIntegerField(default=60,verbose_name='耐用月数')
    entrydate=models.DateField(default=timezone.now,verbose_name='进厂日期')
    createtime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    
    def __str__(self):
        return '%s(%s)'% (self.scode,self.sname)
    
    class Meta:
        verbose_name = '701固定资产'
        verbose_name_plural = '701固定资产'


class equipment(models.Model):
    cate=(
    ('1',u'运行中'),
    ('2',u'维修中'),
    ('3',u'保养中'),
    ('4',u'闲置中'),
    ('5',u'验收中'),
    ('6',u'校验中'),  
    )
    ecode=models.CharField(max_length=40,primary_key=True,verbose_name='设备编码',help_text='此处以资产编号替代设备编号')
    ename=models.CharField(max_length=80,verbose_name='设备名称')
    status=models.CharField(max_length=40,choices=cate,default='4',verbose_name='当前状态')
    station=models.CharField(max_length=80,default='工具室',verbose_name='使用地点',help_text='以部门/Cell-工站-识别号 方式进行地点编码。')
    MEG=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='equipment',verbose_name='设备工程师')   
    remark=models.TextField(null=True,blank=True,verbose_name='说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="更新者")
    userguide=models.FileField(upload_to = 'Equipment/UserGuide/%Y%m%d/',null=True,blank=True,verbose_name='用户手册')
    
    def __str__(self):
        return '%s(%s)'% (self.ecode,self.ename)
    
    class Meta:
        verbose_name = '702设备主档'
        verbose_name_plural = '702设备主档'


class station(models.Model):
    station=models.CharField(max_length=80,primary_key=True,verbose_name='位置编码')
    dep=models.ForeignKey(department,on_delete=models.DO_NOTHING, limit_choices_to= ~Q(category='C'),blank=True, null=True,related_name='station1', verbose_name='部门')
    cell=models.ForeignKey(department,on_delete=models.DO_NOTHING, limit_choices_to= Q(category='C'),blank=True, null=True,related_name='station2', verbose_name='Cell')
    operation=models.ForeignKey(operation,on_delete=models.DO_NOTHING,limit_choices_to= Q(category='2'),blank=True, null=True,related_name='station3', verbose_name='工作中心')
    location=models.CharField(max_length=40,default=1,verbose_name='区别码',help_text='当同一个工作中心，有多个工站时，使用区别码')
    PIC=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='station4',verbose_name='保管人') 
    stationdesc=models.TextField(null=True,blank=True,verbose_name='备注')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return  str(self.station)
    
    class Meta:
        verbose_name = '703工站位置'
        verbose_name_plural = '703工站位置'


class tpmitem(models.Model):
    cate=(
    ('1',u'日常点检'),
    ('2',u'定期保养'),
    ('3',u'预防校验'),
    )
    mcode=models.CharField(max_length=40,verbose_name='设备类')
    mitem=models.CharField(max_length=120,verbose_name='项目')
    mcontent=models.TextField(max_length=120,verbose_name='内容和方法')
    mspec=models.CharField(max_length=120,verbose_name='标准要求')
    category=models.CharField(max_length=20,default=1,choices=cate,verbose_name='分类')
    period=models.SmallIntegerField(default=1,verbose_name='间隔天数')
    createtime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s(%s)'%(self.mcode,self.mitem)
    
    class Meta:
        verbose_name = '704维护项目'
        verbose_name_plural = '704维护项目'




class category(models.Model):
    tcode=models.CharField(max_length=40,primary_key=True,verbose_name='编码')
    tname=models.CharField(max_length=80,unique=True,verbose_name='分类')
    tdesc=models.TextField(null=True,blank=True,verbose_name='说明')
    userguide=models.FileField(upload_to = 'TPM/UserGuide/%Y%m%d/',null=True,blank=True,verbose_name='用户手册')
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,verbose_name='主分类')    
    tpm=models.ManyToManyField('tpmitem',related_name='tpmcategory1',null=True,blank=True,verbose_name='TPM项目')
    equipment=models.ManyToManyField('equipment',related_name='tpmcategory2',null=True,blank=True,verbose_name='设备清单')
    createtime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.tname)
    
    class Meta:
        verbose_name = '705设备分类'
        verbose_name_plural = '705设备分类'


class runstatus(models.Model):
    equipment=models.ForeignKey('equipment',on_delete=models.CASCADE,related_name='runstatus',verbose_name='设备')
    status=models.CharField(max_length=40,verbose_name='状态',help_text='1：运行，2：维修，3：保养，4：闲置，5：验收，6：校验')
    station=models.CharField(max_length=80,verbose_name='位置')
    starttime=models.DateTimeField(default=timezone.now,verbose_name='开始时间')
    endtime=models.DateTimeField(null=True,blank=True,verbose_name='结束时间')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")

    def __str__(self):
        return str(self.equipment)
    
    class Meta:
        verbose_name = '706运行状态'
        verbose_name_plural = '706运行状态'


class tpmrecords(models.Model):
    tpmdate=models.DateField(default=timezone.now,verbose_name='日期')
    equipment=models.ForeignKey('equipment',on_delete=models.CASCADE,related_name='tpmrecords1',verbose_name='设备')
    item=models.ForeignKey('tpmitem',on_delete=models.DO_NOTHING,related_name='tpmrecords2',verbose_name='项目')
    judge=models.BooleanField(default=1,verbose_name='判定')
    remark=models.CharField(max_length=200,null=True,blank=True,verbose_name='备注')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")
    createtime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s(%s)'% (self.equipment,self.item)
    
    class Meta:
        verbose_name = '707检修记录'
        verbose_name_plural = '707检修记录'


class troublecode(models.Model):
    troublecode=models.CharField(max_length=40,primary_key=True,verbose_name='故障代码')
    troublename=models.CharField(max_length=80,verbose_name='故障状况')
    PIC=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='troublecode',verbose_name='维修人')  
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.troublename)
    
    class Meta:
        verbose_name = '708故障代码'
        verbose_name_plural = '708故障代码'


class troublerecords(models.Model):
    dis=(    
    ('1',u'厂内维修'),
    ('2',u'发外维修'),
    ('3',u'限制使用'),
    ('4',u'申请报废'),
    ('0',u'其它'),
    )
    sta=(
    ('1',u'故障确认中'),
    ('2',u'方案审核中'),
    ('3',u'设备维修中'),
    ('4',u'设备验收中'),
    ('5',u'结案'),
    )
    equipment=models.ForeignKey('equipment',on_delete=models.CASCADE,related_name='troublerecords1',verbose_name='设备')
    trouble=models.ForeignKey('troublecode',on_delete=models.DO_NOTHING,related_name='troublerecords2',verbose_name='故障')
    troubledesc=models.TextField(blank=True,null=True,verbose_name='故障描述')
    createname=models.CharField(max_length=40, blank=True,verbose_name="故障发现者")
    updatetime=models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name='发现时间')
    confirm=models.CharField(max_length=40,blank=True,verbose_name='故障确认者')
    Repair=models.TextField(blank=True,verbose_name='修复方案')
    confirmtime=models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name='确认时间')
    dispose=models.CharField(max_length=80,default=1,choices=dis,verbose_name='处置措施')
    status=models.CharField(max_length=40,default=1,choices=sta,verbose_name='处置状态')
    remark=models.TextField(blank=True,verbose_name='备注')
    updatetime=models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name='更新时间')
 
    def __str__(self):
        return '%s(%s)'% (self.equipment,self.trouble)
    
    class Meta:
        verbose_name = '709故障记录'
        verbose_name_plural = '709故障记录'


