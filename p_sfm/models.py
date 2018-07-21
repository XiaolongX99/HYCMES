# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from p_admin.models import department,organization
from p_pdm.models import operation,producttree,pcode
from p_opm.models import org,group
from django.contrib.auth.models import User
from django.db.models import When, F, Q


#生产派工
class dispatch(models.Model):
    dpid=models.CharField(primary_key=True,max_length=80,verbose_name='派工码')
    PL=models.CharField(max_length=40,null=True,verbose_name='部门')
    cell=models.CharField(max_length=40,null=True,verbose_name='Cell')
    operation=models.CharField(max_length=40,null=True,verbose_name='工站') 
    po=models.CharField(null=True,max_length=40,verbose_name='订单')
    poid=models.CharField(null=True,blank=True,max_length=40,verbose_name='订单项次')
    item=models.CharField(null=True,max_length=40,verbose_name='料号')    
    wo=models.CharField(null=True,max_length=40,verbose_name='工单')
    startqty=models.SmallIntegerField(default=1,verbose_name='派工数量')
    completeqty=models.SmallIntegerField(default=0,verbose_name='完工数量')
    startdate=models.DateField(default=timezone.now,verbose_name='开工日期')
    completedate=models.DateField(null=True,blank=True,verbose_name='完工日期')
    states=models.SmallIntegerField(default='1',verbose_name='状态码',help_text='1:正常派单，2：返工派单, 99：生产完工，0：取消派单')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.dpid)
    
    class Meta:
        verbose_name = '101生产派工'
        verbose_name_plural = '101生产派工'

#派工序号
class dispatchsn(models.Model):
    dpid=models.ForeignKey('dispatch',on_delete=models.CASCADE,related_name='dispatchsn',verbose_name='派工码')
    sn=models.CharField(primary_key=True,max_length=40,verbose_name='识别序号')
    lotsize=models.SmallIntegerField(default=1,verbose_name='批量大小')
    states=models.SmallIntegerField(default='1',verbose_name='派单状态',help_text='1:首次派发，>=2：多次派发，0：拆解流程单')
    dispatch=models.CharField(max_length=200,null=True,verbose_name='当前工序',help_text='移转后更新')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '102派工序号'
        verbose_name_plural = '102派工序号'

#派工制程
class dispatchrouting(models.Model):
    dpid=models.ForeignKey('dispatch',on_delete=models.CASCADE,related_name='dispatchrouting',verbose_name='派工码')
    process=models.ForeignKey(pcode,on_delete=models.DO_NOTHING,related_name='dispatchroutingprocess',verbose_name='生产制程')
    step=models.SmallIntegerField(default=1,verbose_name='作业顺序')
    states=models.TextField(default='1',null=True,verbose_name='流程状态说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.process

    class Meta:
        verbose_name = '103派工制程'
        verbose_name_plural = '103派工制程'
        unique_together=('dpid','process','step')

#派工用料
class dispatchbom(models.Model):
    dpid=models.ForeignKey('dispatch',on_delete=models.CASCADE,related_name='dispatchbom',verbose_name='派工码')
    component=models.CharField(max_length=80,verbose_name='工单材料')
    qty=models.DecimalField(default=1,max_digits=12, decimal_places=4,verbose_name='用料数量')
    lot=models.TextField(null=True,blank=True,verbose_name='用料信息')
    states=models.SmallIntegerField(default='1',verbose_name='状态码',help_text='1:待制，2：在制，3：待检，99:关闭,0：取消')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    #operation=models.CharField(max_length=40,null=True,blank=True,verbose_name='发料工站')

    def __str__(self):
        return self.component

    class Meta:
        verbose_name = '104工单用料'
        verbose_name_plural = '104工单用料'
        unique_together=('dpid','component')

#制程移转
class transfer(models.Model):
    sate=(
    ('0',u'未完工'),
    ('1',u'完工待检'),
    ('99',u'检验合格'),
    ('-1',u'批失效'),
    ) 
    trid=models.CharField(primary_key=True,max_length=40,verbose_name='追溯码')
    workingdate=models.DateField(default=timezone.now,verbose_name='生产日期')
    PL=models.CharField(max_length=40,verbose_name='部门')
    cell=models.CharField(max_length=40,verbose_name='Cell')
    operation=models.CharField(max_length=40,verbose_name='完工工站')
    groups=models.CharField(max_length=40,null=True,verbose_name='群组') 
    po=models.CharField(max_length=40,null=True,verbose_name='订单')
    poid=models.CharField(max_length=40,null=True,verbose_name='订单项次')
    item=models.CharField(max_length=40,null=True,verbose_name='料号')
    wo=models.CharField(max_length=40,null=True,verbose_name='工单')      
    passqty=models.DecimalField(default=1,max_digits=8, decimal_places=2,verbose_name='Pass数量')
    failqty=models.DecimalField(default=0,max_digits=8, decimal_places=2,verbose_name='Fail数量')
    starttime=models.DateTimeField(default=timezone.now,verbose_name='开始时间')
    completetime=models.DateTimeField(default=timezone.now,verbose_name='完成时间')
    states=models.SmallIntegerField(default=1,editable=False,choices=sate,verbose_name='状态码') 
    operatorlist=models.TextField(null=True,blank=True,verbose_name='人员名单')
    processlist=models.TextField(null=True,blank=True,verbose_name='制程明细') 
    remark=models.TextField(null=True,blank=True,verbose_name='移转说明')

    def __str__(self):
        return str(self.trid)
    
    class Meta:
        verbose_name = '105生产移转'
        verbose_name_plural = '105生产移转'
        ordering = ['workingdate','PL','cell','operation'] 


#SN移转记录
class transfersn(models.Model):
    trid=models.ForeignKey('transfer',on_delete=models.CASCADE,related_name='batch',verbose_name='追溯码')
    sn=models.CharField(max_length=40,verbose_name='识别序号')   
    passqty=models.DecimalField(default=1,max_digits=8, decimal_places=2,verbose_name='良品数量')
    failqty=models.DecimalField(default=0,max_digits=8, decimal_places=2,verbose_name='失效数量')
    operation=models.CharField(max_length=40,null=True,verbose_name='转入工站')
    operator=models.TextField(null=True,verbose_name='作业人员')
    states=models.CharField(max_length=40,default='1',verbose_name='状态',help_text='与派单状态相同')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.sn
    
    class Meta:
        unique_together=('trid','sn',)
        verbose_name = '106移转序号'
        verbose_name_plural = '106移转序号'


#用料记录
class transfertracking(models.Model):
    cate=(
    ('1',u'待检'),
    ('2',u'退换料'),
    ('3',u'报废'),
    ('4',u'回收'),
    ('5',u'其它'),
    ('0',u'取消记录'),
    ) 
    trid=models.ForeignKey('transfer',on_delete=models.CASCADE,related_name='tracking',verbose_name='追溯码')
    component=models.CharField(max_length=40,verbose_name='材料品号')    
    lot=models.CharField(max_length=120,null=True,blank=True,verbose_name='材料批号')
    failqty=models.CharField(max_length=40,default='0',null=True,blank=True,verbose_name='损耗数',help_text='材料不良情况为损耗，正常损耗=0.')
    faildesc=models.TextField(null=True,blank=True,verbose_name='损耗说明')
    states=models.SmallIntegerField(default='1',choices=cate,verbose_name='处理状态',help_text='1:待检，2：退换料，3：报废，4: 回收,0：取消记录')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.component

    class Meta:
        verbose_name = '107用料记录'
        verbose_name_plural = '107用料记录'


#参数记录
class transferparameter(models.Model):
    trid=models.ForeignKey('transfer',on_delete=models.CASCADE,related_name='processparameter',verbose_name='追溯码')
    sn=models.CharField(max_length=40,null=True,blank=True,verbose_name='识别序号')
    parameter=models.CharField(max_length=40,verbose_name='参数')    
    pvalue=models.CharField(max_length=200,null=True,blank=True,verbose_name='参数值')
    pdesc=models.CharField(max_length=200,null=True,blank=True,verbose_name='记录描述')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.parameter
    
    class Meta:
        verbose_name = '115制程参数记录'
        verbose_name_plural = '115制程参数记录'


#失效模式
class modelfail(models.Model):
    failcode=models.CharField(max_length=40,primary_key=True,verbose_name='不良代码')
    faildesc=models.TextField(null=True,verbose_name='不良说明')
    operation=models.ForeignKey(operation,on_delete=models.DO_NOTHING,null=True,blank=True,limit_choices_to=Q(category='2'),related_name='failmodeoperation',verbose_name='工作中心')
    product=models.ForeignKey(producttree,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='failmodeproducttree',verbose_name='产品群')
    responder=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='PLFMResponderuser',verbose_name='回应者',help_text='选择人员后，发生此项异常时，系统自动通知回应者')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.failCode

    class Meta:
        verbose_name = '108不良代码'
        verbose_name_plural = '108不良代码'


#失效明细
class transferfail(models.Model):
    cate=(
    ('1',u'待检'),
    ('2',u'返工'),
    ('3',u'回收'),
    ('4',u'其它'),
    ('0',u'取消记录'),
    )   
    trid=models.ForeignKey('transfer',on_delete=models.CASCADE,related_name='faildetail',verbose_name='追溯码')
    sn=models.CharField(max_length=40,null=True,blank=True,verbose_name='识别序号')    
    failcode=models.CharField(max_length=200,null=True,blank=True,verbose_name='不良代码')
    failqty=models.SmallIntegerField(default=1,verbose_name='不良数量')    
    faildesc=models.TextField(null=True,blank=True,verbose_name='不良说明')
    states=models.CharField(default=1,max_length=40,choices=cate,verbose_name='处置状态')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '109不良记录'
        verbose_name_plural = '109不良记录'

#缺失代码
class modelqc(models.Model):   
    qccode=models.CharField(max_length=40,primary_key=True,verbose_name='缺失代码')
    qcdesc=models.TextField(null=True,verbose_name='缺失说明')
    operation=models.ForeignKey(operation,on_delete=models.DO_NOTHING,null=True,blank=True,limit_choices_to=Q(category='2'),related_name='Qoperation',verbose_name='工作中心')
    product=models.ForeignKey(producttree,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='Qproducttree',verbose_name='产品群')
    responder=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='FQCFMResponderuser',verbose_name='回应者',help_text='选择人员后，发生此项异常时，系统自动通知回应者')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.qcode

    class Meta:
        verbose_name = '110缺失代码'
        verbose_name_plural = '110缺失代码'

#QC明细
class transferqc(models.Model):
    cate=(
    ('1',u'合格'),
    ('2',u'条件充收'),
    ('-1',u'批退') 
    )   
    trid=models.ForeignKey('transfer',on_delete=models.CASCADE,related_name='fqcdetail',verbose_name='追溯码')
    completeqty=models.SmallIntegerField(verbose_name='送检数量')
    qcqty=models.SmallIntegerField(verbose_name='检验数量')
    failqty=models.SmallIntegerField(verbose_name='缺失数量')
    qccode=models.CharField(max_length=40,verbose_name='缺失代码')
    qcdesc=models.TextField(null=True,blank=True,verbose_name='检验说明')
    result=models.CharField(default=1,max_length=40,choices=cate,verbose_name='结果判定')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.trid

    class Meta:
        verbose_name = '111FQC记录'
        verbose_name_plural = '111FQC记录'


#产品序号
class productsn(models.Model):
    trsn=models.ForeignKey('dispatchsn',on_delete=models.CASCADE,related_name='shippingsn',verbose_name='识别序号')
    prsn=models.CharField(primary_key=True,max_length=40,verbose_name='产品序号')
    lotsize=models.DecimalField(default=1, max_digits=8, decimal_places=0,verbose_name='产品数量')
    states=models.SmallIntegerField(default='1',verbose_name='状态码',help_text='1:制程中，9：完工入库，99：已出货，-1：成品退回')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.prsn

    class Meta:
        verbose_name = '112出货序号'
        verbose_name_plural = '112出货序号'
        ordering = ['trsn','prsn'] 


#总工时
class CELLHR(models.Model):
    workingdate=models.DateField(default=timezone.now,verbose_name='生产日期')
    PL=models.CharField(max_length=40,verbose_name='部门')
    cell=models.CharField(max_length=40,verbose_name='Cell')
    members=models.SmallIntegerField(default=1,verbose_name='出勤人数')
    workinghours=models.DecimalField(default=8, max_digits=8, decimal_places=2,verbose_name='出勤工时')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '113总工时'
        verbose_name_plural = '113总工时'
