# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone


class warehouse(models.Model):
    code=models.CharField(primary_key=True,max_length=40,verbose_name='仓库编码')
    name=models.CharField(max_length=80,verbose_name='仓库名称')
    FA=models.CharField(max_length=80,null=True,blank=True,verbose_name='财务')
    wmsdesc=models.TextField(null=True,blank=True,verbose_name='说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='601仓库定义'
        verbose_name_plural='601仓库定义'


class locator(models.Model):
    code=models.CharField(primary_key=True,max_length=40,verbose_name='储位编码')
    name=models.CharField(max_length=80,verbose_name='储位名称')
    Xaxis=models.DecimalField(max_digits=12, decimal_places=3,default=1,verbose_name='X坐标')
    Yaxis=models.DecimalField(max_digits=12, decimal_places=3,default=1,verbose_name='Y坐标')
    Zaxis=models.DecimalField(max_digits=12, decimal_places=3,default=1,verbose_name='Z坐标')
    length=models.DecimalField(max_digits=12, decimal_places=3,default=1,verbose_name='储位长(m)')
    width=models.DecimalField(max_digits=12, decimal_places=3,default=1,verbose_name='储位宽(m)')
    heigth=models.DecimalField(max_digits=12, decimal_places=3,default=1,verbose_name='储位高(m)')
    states=models.SmallIntegerField(default=1,verbose_name='储位状态')
    parent=models.ForeignKey('warehouse',on_delete=models.DO_NOTHING,related_name='locator',verbose_name='所属仓库')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='602储位定义'
        verbose_name_plural='602储位定义'


class transaction(models.Model):
    cate=(
    ('1', u'入库'),
    ('-1', u'出库')
    )
    IO=models.CharField(max_length=4,choices=cate,verbose_name='作业')
    item=models.CharField(max_length=40,verbose_name='料号')
    lot=models.CharField(max_length=120,null=True,blank=True,verbose_name='批号')
    warehouse=models.ForeignKey('warehouse',on_delete=models.DO_NOTHING,related_name='transactionw',verbose_name='仓库')
    locator=models.ForeignKey('locator',on_delete=models.DO_NOTHING,related_name='transactionl',verbose_name='储位')
    qty=models.DecimalField(max_digits=12, decimal_places=4,default=0,verbose_name='进出数量')
    capacity=models.DecimalField(max_digits=8, default=0,decimal_places=4,null=True,blank=True,verbose_name='占用空间')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    updatename=models.CharField(max_length=40,null=True,verbose_name='操作者')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name='603出入库'
        verbose_name_plural='603出入库'


class storage(models.Model):
    item=models.CharField(max_length=40,verbose_name='料号')
    lot=models.CharField(max_length=120,null=True,verbose_name='批号')
    warehouse=models.ForeignKey('warehouse',on_delete=models.DO_NOTHING,related_name='storagew',verbose_name='仓库')
    locator=models.ForeignKey('locator',on_delete=models.DO_NOTHING,related_name='storagel',verbose_name='储位')
    qty=models.DecimalField(max_digits=12, decimal_places=4,default=0,verbose_name='进出数量')
    capacity=models.DecimalField(max_digits=8, decimal_places=4,default=0,verbose_name='占用空间')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name='604当前存货'
        verbose_name_plural='604当前存货'
        unique_together=('item','lot','warehouse','locator')


class item(models.Model):
	item=models.CharField(primary_key=True,max_length=40,verbose_name='料号')
	itemdesc=models.CharField(max_length=200,verbose_name='物料说明')
	uom=models.CharField(max_length=40,verbose_name='单位')
	volume=models.DecimalField(max_digits=12, decimal_places=6,null=True,blank=True,verbose_name='体积(立方米)')
	weight=models.DecimalField(max_digits=12, decimal_places=6,null=True,blank=True,verbose_name='重量(千克)')
	minqty=models.DecimalField(max_digits=12, decimal_places=4,null=True,blank=True,verbose_name='最小存量')
	maxqty=models.DecimalField(max_digits=12, decimal_places=4,null=True,blank=True,verbose_name='最大存量')
	validity=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,verbose_name='有效期(天)')
	lotcontrol=models.BooleanField(default=False,verbose_name='批号管制')
	warehouse=models.ForeignKey('warehouse',on_delete=models.DO_NOTHING,related_name='itemw',verbose_name='仓库')
	locator=models.ManyToManyField('locator',null=True,blank=True,related_name='iteml',verbose_name='默认储位')
	updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

	def __str__(self):
		return self.item

	class Meta:
		verbose_name='605存储属性'
		verbose_name_plural='605存储属性'