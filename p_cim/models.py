from django.db import models
from django.utils import timezone




class TemplateSN(models.Model):
	template=models.CharField(max_length=80,verbose_name='模版')
	item=models.CharField(max_length=120,null=True,blank=True,verbose_name='项目')
	Xaxis=models.SmallIntegerField(verbose_name='Rows行座标')
	Yaxis=models.SmallIntegerField(verbose_name='Columns列座标')
	TS01=models.CharField(max_length=80, null=True, blank=True,verbose_name='参数01')
	TS02=models.CharField(max_length=80, null=True, blank=True,verbose_name='参数02')
	TS03=models.CharField(max_length=80, null=True, blank=True,verbose_name='参数03')
	TS04=models.CharField(max_length=80, null=True, blank=True,verbose_name='参数04')
	TS05=models.CharField(max_length=80, null=True, blank=True,verbose_name='参数05')
	TS06=models.CharField(max_length=80, null=True, blank=True,verbose_name='参数06')
	updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

	def __str__(self):
		return str(self.item)
    
	class Meta:
		verbose_name = '1001模版'
		verbose_name_plural = '1001模版'


class TestSN(models.Model):
	sn=models.CharField(primary_key=True,max_length=80,verbose_name='序号')
	product=models.CharField(max_length=120,null=True,blank=True,verbose_name='产品')
	po=models.CharField(max_length=80,null=True,blank=True,verbose_name='订单')
	poid=models.CharField(max_length=40,null=True,blank=True,verbose_name='订单项次')
	item=models.CharField(max_length=80,null=True,blank=True,verbose_name='料号')    
	states=models.SmallIntegerField(default='1',verbose_name='状态码',help_text='1:正常，-1：不良, 99：完工，0：删除')
	updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
	PC01=models.CharField(max_length=80, null=True, verbose_name='PC01')
	PC02=models.CharField(max_length=80, null=True, verbose_name='PC02')
	PC03=models.CharField(max_length=80, null=True, verbose_name='PC03')
	PC04=models.CharField(max_length=80, null=True, verbose_name='PC04')
	PC05=models.CharField(max_length=80, null=True, verbose_name='PC05')
	PC06=models.CharField(max_length=80, null=True, verbose_name='PC06')

	def __str__(self):
		return self.sn
    
	class Meta:
		verbose_name = '1002测试序号'
		verbose_name_plural = '1002测试序号'


class TestRowData(models.Model):
	SN=models.CharField(max_length=80,verbose_name='序号')
	Channel=models.CharField(max_length=80,null=True,blank=True,verbose_name='通道')
	Parameter=models.CharField(max_length=80,null=True,blank=True,verbose_name='参数')
	Value=models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='数值')
	Judge=models.BooleanField(default=True,verbose_name='判定结果')
	updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
	PA01=models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='PA01')
	PA02=models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='PA02')
	PA03=models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='PA03')
	PA04=models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='PA04')
	PA05=models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='PA05')
	PA06=models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='PA06')
	PB01=models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name='PB01')
	PB02=models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name='PB02')
	PB03=models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name='PB03')
	PB04=models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name='PB04')
	PB05=models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name='PB05')
	PB06=models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name='PB06')
	PC01=models.CharField(max_length=80, null=True, verbose_name='PC01')
	PC02=models.CharField(max_length=80, null=True, verbose_name='PC02')
	PC03=models.CharField(max_length=80, null=True, verbose_name='PC03')
	PC04=models.CharField(max_length=80, null=True, verbose_name='PC04')
	PC05=models.CharField(max_length=80, null=True, verbose_name='PC05')
	PC06=models.CharField(max_length=80, null=True, verbose_name='PC06')

	def __str__(self):
		return '%s(%s)' %(self.SN,self.Channel)
    
	class Meta:
		verbose_name = '1003PLC测试数据'
		verbose_name_plural = '1003测试数据'

