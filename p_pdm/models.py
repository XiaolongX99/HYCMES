# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from p_admin.models import department
from django.utils import timezone
from django.db.models import When, F, Q


class productgroup(models.Model):
    groupcode=models.CharField(max_length=40,primary_key=True,verbose_name='产品族编码')
    groupname=models.CharField(max_length=80,unique=True,verbose_name='产品族名称')
    PM=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='productgrouppm',verbose_name='产品经理')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s(%s)'% (self.groupname,self.groupcode)
    
    class Meta:
        verbose_name = '201产品族'
        verbose_name_plural = '201产品族'
        ordering = ['groupcode','PM'] 


class producttree(models.Model):
    productcode=models.CharField(max_length=40,primary_key=True,verbose_name='产品群编码')
    productname=models.CharField(max_length=80,unique=True,verbose_name='产品群名称')
    parent=models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name='父级群')
    PDE=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='producttreepde',verbose_name='产品工程师')
    PG=models.ForeignKey('productgroup',on_delete=models.DO_NOTHING,related_name='pgs',verbose_name='产品族')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    operation=models.ManyToManyField('operation',null=True,blank=True,limit_choices_to=Q(category='2'),related_name='productreeoperation',verbose_name='工作中心')
    process=models.ManyToManyField('operation',null=True,blank=True,limit_choices_to=Q(category='3'),related_name='productreepcode',verbose_name='作业制程')
    item=models.ManyToManyField('item',null=True,blank=True,related_name='productreeitem',verbose_name='产品号(群)')

    def __str__(self):
        return '%s(%s)'% (self.productname,self.productcode)
    
    class Meta:
        verbose_name = '202产品群'
        verbose_name_plural = '202产品群'
        ordering = ['productcode'] 


class item(models.Model):
    item=models.CharField(max_length=80,primary_key=True,verbose_name='产品码')
    itemgroup=models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='itemgroups',verbose_name='途程')
    states=models.BooleanField(default='1',verbose_name='状态')
    productgroup=models.ForeignKey('producttree',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='itempgs',verbose_name='产品群')
    itemdesc=models.TextField(null=True,blank=True,verbose_name='产品描述')
    itemspec=models.TextField(null=True,blank=True,verbose_name='产品规格')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    route=models.ManyToManyField('pcode',through='itempcode',null=True,blank=True,verbose_name='途程')
    

    def __str__(self):
        return str(self.item)

    class Meta:
        verbose_name = '203产品码'
        verbose_name_plural = '203产品码'
        ordering = ['productgroup','item']


class productline(models.Model):
    PL=models.OneToOneField(department,on_delete=models.DO_NOTHING,primary_key=True,limit_choices_to= Q(category='P')|Q(category='C'),related_name='productline',verbose_name='产线')
    ERP=models.CharField(max_length=40,null=True,blank=True,verbose_name='财务代码')
    ADM=models.CharField(max_length=40,null=True,blank=True,verbose_name='行政代码')
    SFM=models.CharField(max_length=40,null=True,blank=True,verbose_name='生产代码')
    APS=models.CharField(max_length=40,null=True,blank=True,verbose_name='计划代码')
    OPM=models.CharField(max_length=40,null=True,blank=True,verbose_name='绩效代码')
    WMS=models.CharField(max_length=40,null=True,blank=True,verbose_name='仓储代码')
    SCM=models.CharField(max_length=40,null=True,blank=True,verbose_name='采购代码')
    PDM=models.CharField(max_length=40,null=True,blank=True,verbose_name='工程代码')
    MES=models.CharField(max_length=40,null=True,blank=True,verbose_name='系统代码')
    operation=models.ManyToManyField('operation',null=True,blank=True,limit_choices_to=Q(category='2'),verbose_name='工作中心')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.PL)
    
    class Meta:
        verbose_name = '204产品线'
        verbose_name_plural = '204产品线'
        ordering = ['PL'] 


class operation(models.Model):
    cate=(
    ('1',u'虚设'),
    ('2',u'标准'),
    ('3',u'专属'),
    )
    opcode=models.CharField(max_length=40,primary_key=True,verbose_name='工作编码')
    opname=models.CharField(max_length=80,verbose_name='工作中心')
    category=models.CharField(max_length=40,choices=cate,null=True,blank=True,verbose_name='类别')
    parent=models.ForeignKey('self',on_delete=models.DO_NOTHING,related_name='parents',null=True,blank=True,limit_choices_to=Q(category=1) | Q(category=2),verbose_name='父级站')
    PCE=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='operationpce',verbose_name='制程工程师')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    process=models.ManyToManyField('process',null=True,blank=True,verbose_name='作业参数')

    def __str__(self):
        return '%s(%s)'% (self.opname,self.opcode)

    class Meta:
        verbose_name = '205工作中心'
        verbose_name_plural = '205工作中心'
        ordering = ['category','opcode'] 


class process(models.Model):
    process=models.CharField(max_length=40,primary_key=True,verbose_name='工作参数')
    prodesc=models.TextField(null=True,verbose_name='参数说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s(%s)'% (self.process,self.prodesc)
    
    class Meta:
        verbose_name = '206工作参数'
        verbose_name_plural = '206工作参数'


class pcode(models.Model):
    pcode=models.CharField(max_length=40,primary_key=True,verbose_name='作业代码')
    pname=models.CharField(max_length=80,verbose_name='作业名称')    
    labor=models.DecimalField(max_digits=8, decimal_places=0,null=True,blank=True,verbose_name='作业工时(单位：秒)')
    operation=models.ForeignKey('operation',on_delete=models.DO_NOTHING,limit_choices_to=Q(category='2'),null=True,blank=True,related_name='pcode',verbose_name='所属工作中心')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    
    def __str__(self):
        return str(self.pname)
    
    class Meta:
        verbose_name = '207制程标准'
        verbose_name_plural = '207制程标准'


class pcoderev(models.Model):
    pcode=models.CharField(max_length=40,verbose_name='作业代码')
    pname=models.CharField(max_length=40,verbose_name='作业名称') 
    labor=models.DecimalField(max_digits=8, decimal_places=0,null=True,verbose_name='作业工时(单位：秒)')
    changes=models.TextField(null=True,verbose_name='修订原因')
    states=models.SmallIntegerField(null=True,verbose_name='标准版次')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='修订时间')
    updatename=models.CharField(max_length=40, blank=True,null=True,verbose_name="修订者")
    
    def __str__(self):
        return str(self.pname)
    
    class Meta:
        verbose_name = '208标准修订'
        verbose_name_plural = '208标准修订'
        ordering = ['pcode','states'] 
        unique_together = ('pcode','updatetime')


#产品制程
class itempcode(models.Model):
    item=models.ForeignKey('item',on_delete=models.CASCADE,related_name='itempocdepcode1',verbose_name='料号')
    pcode=models.ForeignKey('pcode',on_delete=models.DO_NOTHING,related_name='itempocdepcode2',verbose_name='作业')
    step=models.SmallIntegerField(default=1,null=True,verbose_name='作业步骤')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")
    parameter=models.ManyToManyField('parameter',through='itempcodespec',verbose_name='参数')

    def __str__(self):
        return '%s(%s)'%(self.item,self.pcode)

    class Meta:
        verbose_name = '209产品途程'
        verbose_name_plural = '209产品途程'
        ordering = ['item','step'] 
        unique_together = ('item','pcode')


#参数定义
class parameter(models.Model):
    cate=(
    ('1',u'通用参数'),
    ('2',u'标准参数'),
    )
    parameter=models.CharField(primary_key=True,max_length=40,verbose_name='参数')
    spec=models.CharField(max_length=200,null=True,blank=True,verbose_name='描述')
    pmproperty=models.CharField(max_length=20,default=1,choices=cate,null=True,verbose_name='特征',help_text="1:通用参数，如进出烘箱时间；2:标准参数，如产品测试值。")
    process=models.ForeignKey('operation',on_delete=models.DO_NOTHING,null=True,blank=True,limit_choices_to=Q(category='2'),related_name='parameter',verbose_name='所属')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s(%s)'%(self.parameter,self.pmproperty)
    
    class Meta:
        verbose_name = '210参数定义'
        verbose_name_plural = '210参数定义'


#制程规格
class itempcodespec(models.Model):
    route=models.ForeignKey('itempcode',on_delete=models.DO_NOTHING,related_name='specroute',verbose_name='途程')
    parameter=models.ForeignKey('parameter',on_delete=models.DO_NOTHING,related_name='specparam',verbose_name='参数')
    spec=models.CharField(max_length=200,null=True,blank=True,verbose_name='单位')
    UCL=models.DecimalField(default=0, max_digits=8, decimal_places=2,null=True,blank=True,verbose_name='上限值')
    CL=models.DecimalField(default=0, max_digits=8, decimal_places=2,null=True,blank=True,verbose_name='中心值')
    LCL=models.DecimalField(default=0, max_digits=8, decimal_places=2,null=True,blank=True,verbose_name='下限值')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.parameter)
    
    class Meta:
        unique_together=('route','parameter',)
        verbose_name = '211途程参数'
        verbose_name_plural = '211途程参数'


#产品用料
class itembom(models.Model):
    item=models.CharField(max_length=80,verbose_name='主件')
    seq=models.SmallIntegerField(verbose_name='序号')
    component=models.CharField(max_length=80,verbose_name='零件')
    componentdesc=models.TextField(null=True,blank=True,verbose_name='描述')
    componentspec=models.TextField(null=True,blank=True,verbose_name='规格')
    qty=models.DecimalField(default=1,max_digits=12, decimal_places=4,verbose_name='用料数量')
    loss=models.DecimalField(default=0,max_digits=8, decimal_places=4,verbose_name='损耗量')
    units=models.CharField(default='PCS',max_length=40,verbose_name='用料单位')
    starttime=models.DateField(default=timezone.now,verbose_name='生效时间')
    endtime=models.DateField(blank=True,null=True,verbose_name='失效时间')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '212产品用料'
        verbose_name_plural = '212产品用料'
        ordering = ['item','component'] 
        unique_together = ('item','component')

#头数
class bomport(models.Model):
    item=models.CharField(max_length=80,primary_key=True,verbose_name='料号')
    port=models.SmallIntegerField(default=1,verbose_name='接头数')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return  '%s(%s)'% (self.item,self.port)

    class Meta:
        verbose_name = '213产品头数'
        verbose_name_plural = '213产品头数'
        