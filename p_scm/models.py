# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
#SCM models

class rfqgroup(models.Model):
    cate=(
    ('R',u'时间'),
    ('F',u'频率'),
    ('Q',u'数量'),
    ('M',u'金额')  
    )
    gp=(    
    ('0.01',u'1'),
    ('0.1',u'2'),
    ('1.0',u'3'),
    ('2.0',u'4'),
    ('3.0',u'5'),
    ('4.0',u'6'),
    ('5.0',u'7')  
    )
    category=models.CharField(max_length=40,choices=cate,verbose_name='分类')
    group=models.CharField(max_length=40,choices=gp,verbose_name='分组')
    groupvalue=models.DecimalField(max_digits=12, decimal_places=2,verbose_name='组值')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = '501RFM分组'
        verbose_name_plural = '501RFM分组'
        ordering = ['category','group'] 
        unique_together =('category','group',)

class rfqdata(models.Model):
    category1=models.CharField(max_length=40,null=True,verbose_name='分类1')
    category2=models.CharField(max_length=40,null=True,verbose_name='分类2')
    category3=models.CharField(max_length=40,null=True,verbose_name='分类3')
    item=models.CharField(max_length=40,verbose_name='料号')
    R=models.DecimalField(max_digits=12, decimal_places=2,verbose_name='时间')
    F=models.DecimalField(max_digits=12, decimal_places=2,verbose_name='频率')
    Q=models.DecimalField(max_digits=12, decimal_places=2,verbose_name='数量')
    M=models.DecimalField(max_digits=12, decimal_places=2,verbose_name='金额')
    RG=models.DecimalField(max_digits=4, decimal_places=2,null=True,verbose_name='时间分组')
    FG=models.DecimalField(max_digits=4, decimal_places=2,null=True,verbose_name='频率分组')
    QG=models.DecimalField(max_digits=4, decimal_places=2,null=True,verbose_name='数量分组')
    MG=models.DecimalField(max_digits=4, decimal_places=2,null=True,verbose_name='金额分组')
    rfq=models.DecimalField(max_digits=12, decimal_places=6,verbose_name='RFQ')
    rfm=models.DecimalField(max_digits=12, decimal_places=6,verbose_name='RFM')   

    def __str__(self):
        return self.item
    
    class Meta:
        verbose_name = '502RFQ数据'
        verbose_name_plural = '502RFQ数据'
        ordering = ['item'] 
