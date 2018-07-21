# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from p_admin.models import department,organization,axisdate,axistime
from p_pdm.models import operation



class demand(models.Model):
    po=models.CharField(max_length=40,verbose_name='订单')
    poid=models.CharField(max_length=40,verbose_name='订单项次')
    customerid=models.CharField(max_length=40,verbose_name='客户编码')
    customeritem=models.CharField(max_length=80,verbose_name='客户料号')
    item=models.CharField(max_length=80,verbose_name='产品料号')
    itemdesc=models.TextField(verbose_name='产品描述')
    itemspec=models.TextField(verbose_name='产品规格')
    demandqty=models.IntegerField(verbose_name='需求数量')
    shipqty=models.IntegerField(verbose_name='出货数量')
    podate=models.DateField(verbose_name='订单日期')
    demanddate=models.DateField(verbose_name='需求日期')
    states=models.CharField(max_length=40,verbose_name='订单状态')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%s'%(self.po,self.poid)

    class Meta:
        verbose_name = '401客户订单'
        verbose_name_plural = '401客户订单'
        ordering = ['po','poid']


class atp(models.Model):
    dep=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'P'},related_name='atpdep',verbose_name='部门')
    cell=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'C'},related_name='atpcell',verbose_name='Cell')
    period=models.CharField(max_length=40,verbose_name='时期',help_text='时期：可以是1天，也可以是1周或1月，任意天数时期序列。')
    poqty=models.IntegerField(verbose_name='订单数量')
    forecastqty=models.IntegerField(verbose_name='预测数量')
    supplyqty=models.IntegerField(verbose_name='外购数量')
    productionqty=models.IntegerField(verbose_name='生产数量')
    ATP=models.IntegerField(verbose_name='ATP')
    states=models.CharField(max_length=40,verbose_name='状态')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%s'%(self.period,self.ATP)

    class Meta:
        verbose_name = '402ATP'
        verbose_name_plural = '402ATP'
        ordering = ['dep','cell','period']


class mps(models.Model):
    dep=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'P'},related_name='mpsdep',verbose_name='部门')
    cell=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'C'},related_name='mpscell',verbose_name='Cell')
    po=models.CharField(max_length=40,verbose_name='订单')
    poid=models.CharField(max_length=40,verbose_name='订单项次')
    item=models.CharField(max_length=80,verbose_name='产品料号')
    pqty=models.IntegerField(verbose_name='生产数量')
    pdate=models.DateField(verbose_name='生产日期')
    states=models.CharField(max_length=40,verbose_name='状态')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%s'%(self.pdate,self.po)

    class Meta:
        verbose_name = '403主排程'
        verbose_name_plural = '403主排程'
        ordering = ['pdate','po','poid']


class rccp(models.Model):
    dep=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'P'},related_name='rccpdep',verbose_name='部门')
    cell=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'C'},related_name='rccpcell',verbose_name='Cell')
    operation=models.ForeignKey(operation,on_delete=models.DO_NOTHING,related_name='rccpoperation',verbose_name='工作中心') 
    upph=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='人时产出(UPPH)')
    cycletime=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='产出节拍')
    takttime=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='需求节拍')
    URT=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='负载率')
    pdate=models.DateField(verbose_name='生产日期')
    states=models.CharField(max_length=40,verbose_name='状态')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%s'%(self.pdate,self.URT)

    class Meta:
        verbose_name = '404粗略产能规划'
        verbose_name_plural = '404粗略产能规划'
        ordering = ['dep','cell','operation']


class shipment(models.Model):
    cate=(
    ('Open',u'准备出货'),
    ('Close',u'出货完结'),
    ('Delay',u'延迟出货'),
    ('Change',u'变更数量'),
    ('Cancel',u'取消出货'),
    )
    item=models.CharField(max_length=40,verbose_name='出货通知单号')
    shippingdate=models.DateField(default=timezone.now,verbose_name='出货日期')
    customer=models.CharField(max_length=40,verbose_name='客户代码')
    po=models.CharField(max_length=40,verbose_name='订单号码')
    poid=models.CharField(max_length=40,verbose_name='项次')
    spec=models.CharField(max_length=200,blank=True,null=True,verbose_name='产品规格')
    qty=models.SmallIntegerField(default=1,verbose_name='出货数量')
    shippingtime=models.DateTimeField(default=timezone.now,blank=True,verbose_name='出货时间')
    shippingmethod=models.CharField(max_length=60,null=True,blank=True,verbose_name='货运方式')
    confirm=models.CharField(max_length=200,null=True,blank=True,verbose_name='实际出货')
    status=models.CharField(max_length=40,default='Open',choices=cate,null=True,blank=True,verbose_name='状态')
    remark=models.TextField(null=True,blank=True,verbose_name='备注')
    updatename=models.CharField(max_length=40, blank=True,verbose_name="添加者")
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.item)

    class Meta:
        verbose_name = '405出货通知'
        verbose_name_plural = '405出货通知'


class packinglist(models.Model):
    item=models.CharField(max_length=40,verbose_name='出货通知单号')
    packingdate=models.DateField(default=timezone.now,verbose_name='装箱日期')    
    customer=models.CharField(max_length=40,verbose_name='客户代码')
    box=models.CharField(max_length=40,verbose_name='箱号')
    po=models.CharField(max_length=40,verbose_name='订单号码')
    poid=models.CharField(max_length=40,verbose_name='项次')
    spec=models.CharField(max_length=200,blank=True,verbose_name='产品规格')
    qty=models.SmallIntegerField(default=100,verbose_name='装箱数量')
    packingmethod=models.CharField(max_length=60,default='自封箱',null=True,blank=True,verbose_name='包装方式')
    boxsize=models.CharField(max_length=60,default='54*54*30',null=True,blank=True,verbose_name='外箱尺寸')
    netweight =models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True,verbose_name='净重')
    weight =models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True,verbose_name='毛重')
    remark=models.TextField(null=True,blank=True,verbose_name='备注')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.item)

    class Meta:
        verbose_name = '406装箱清单'
        verbose_name_plural = '406装箱清单'
        unique_together=('item','po','poid','box')



class packing(models.Model):
    item=models.CharField(max_length=40,default=timezone.now,verbose_name='出货通知单号')
    po=models.CharField(max_length=40,verbose_name='订单号码')
    poid=models.CharField(max_length=40,verbose_name='项次')
    box=models.CharField(max_length=40,default='1',verbose_name='外箱号')
    boxid=models.CharField(max_length=40,default='1',null=True,verbose_name='内箱号')
    pn=models.CharField(max_length=40,verbose_name='料号')
    qty=models.SmallIntegerField(default=100,verbose_name='数量')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')


    def __str__(self):
        return str(self.item)

    class Meta:
        verbose_name = '407装箱清单'
        verbose_name_plural = '407装箱清单'
        unique_together=('item','po','poid','box','boxid')


