# -*- coding:utf-8 -*-
from django.db import models
from p_admin.models import department,organization,axisdate,axistime
from p_pdm.models import pcode,operation
from django.utils import timezone
from django.contrib.auth.models import User,Group
import datetime


#岗位技能
class skill(models.Model):    
    skillcode=models.CharField(max_length=40,primary_key=True,verbose_name='技能代码') 
    skilldesc=models.TextField(null=True,blank=True,verbose_name='技能说明')
    allowance =models.DecimalField(max_digits=4, decimal_places=0,default=0,verbose_name='技能津贴(单位:元)',help_text='针对作业员技能/岗位的补贴，幅度：0-300元')
    kvalue=models.DecimalField(default='1',max_digits=8, decimal_places=4,verbose_name='K值',help_text='新人训练完成后，速度可达的单支工时数。')
    nvalue=models.DecimalField(default='-0.2',max_digits=8, decimal_places=4,verbose_name='n值',help_text='学习曲线y=kx^n，学习速度指数n（数值如-0.1，-0.2，-0.3，-0.4，-0.5）')
    operation=models.ManyToManyField(pcode,blank=True,related_name='skillpcode',verbose_name='含括制程') 
    states=models.BooleanField(default=1,verbose_name='有效') 
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    
    def __str__(self):
        return '%s(%s)'%(self.skilldesc,self.skillcode)

    class Meta:
        verbose_name = '301岗位技能'
        verbose_name_plural = '301岗位技能'
        ordering = ['skillcode',]


#生产人员
class org(models.Model):
    jn=models.OneToOneField(organization,on_delete=models.DO_NOTHING,primary_key=True,related_name='orgjn',verbose_name='工号') 
    group=models.ForeignKey('group',on_delete=models.DO_NOTHING,related_name='orggroup',null=True,blank=True,verbose_name='绩效群组')
    cell=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'C'},related_name='orgcell',null=True,blank=True,verbose_name='Cell')
    operation=models.ForeignKey(operation,on_delete=models.DO_NOTHING,null=True,blank=True,limit_choices_to={'category':'2'},related_name='orgoperation',verbose_name='工作中心')
    skill=models.ManyToManyField('skill',null=True,blank=True,verbose_name='人员技能')    
    states=models.BooleanField(default=1,verbose_name='有效') 
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return str(self.jn)

    class Meta:
        verbose_name = '302生产人员'
        verbose_name_plural = '302生产人员'
        ordering = ['cell','jn']

#绩效群组
class group(models.Model):
    cate=(
    ('0',u'个人方案'),
    ('1',u'团队方案'),
    ('2',u'KPI-1方案'), 
    ('3',u'KPI-2方案'),   
    )
    ye=(
    ('2018',u'2018年'),
    ('2019',u'2019年'),
    ('2020',u'2020年'),
    ('2021',u'2021年')  
    )
    mo=(
    ('1',u'1月'),
    ('2',u'2月'),
    ('3',u'3月'),
    ('4',u'4月'),
    ('5',u'5月'),
    ('6',u'6月'),
    ('7',u'7月'),
    ('8',u'8月'),
    ('9',u'9月'),
    ('10',u'10月'),
    ('11',u'11月'),
    ('12',u'12月')
    )
    groupcode=models.CharField(max_length=40,primary_key=True,verbose_name='编码')
    groupdesc = models.CharField(max_length=80,verbose_name='群组')  
    jn=models.ManyToManyField(organization,through='org',null=True,blank=True,verbose_name='人员')
    AMT=models.CharField(max_length=40,default=1,choices=cate,verbose_name='考核方案')   
    SLP=models.ForeignKey('SLG',on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name='SLP',help_text='技能等级绩效方案')
    KPI=models.ForeignKey('KPI',on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name='KPI',help_text='关键绩效指标方案')
    dep=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'P'},related_name='groupdep',null=True,blank=True,verbose_name='部门') 
    YEA=models.CharField(max_length=10,choices=ye,default=datetime.datetime.now().year,verbose_name='年份')
    MON=models.CharField(max_length=10,choices=mo,default=datetime.datetime.now().month,verbose_name='月份') 
    TXR=models.DecimalField(max_digits=4, decimal_places=0,default=100,verbose_name='调整目标百分比(单位:%)',help_text='针对该群组目标值调整比例，幅度：50%-150%')
    TXD=models.DecimalField(max_digits=8, decimal_places=2,default=0,verbose_name='调整基数金额(单位:元)',help_text='针对该群组人均绩效调整金额，幅度：+/-200元')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    cell=models.ManyToManyField(department,limit_choices_to={'category':'C'},null=True,blank=True,verbose_name='所属线别')

    
    def __str__(self):
        return str(self.groupdesc)

    class Meta:
        verbose_name = '303绩效群组'
        verbose_name_plural = '303绩效群组'

#SLG方案
class SLG(models.Model):
    SLP = models.CharField(max_length=40,unique=True,verbose_name='SLP方案')
    slpdesc = models.TextField(null=True,blank=True,verbose_name='方案说明')    
    releasedate = models.DateField(default=timezone.now, verbose_name='生效日期')
    frame = models.ManyToManyField('SLGFrame',null=True,blank=True,verbose_name='绩效框架')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.SLP

    class Meta:
        verbose_name = '304SLP方案'
        verbose_name_plural = '304SLP方案'

#绩效框架
class SLGFrame(models.Model):
    SLP=models.CharField(max_length=40,verbose_name='SLP方案')
    level=models.IntegerField(verbose_name='等级')
    UPPH=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='等级标准(UPPH)',help_text='3等级设置100，其余等级按阶梯设置，如1：64，2：80，3：100，4：120，5：144')
    Grade=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='激励标准(UPPH)',help_text='UPPH达到起点后才开始计算绩效奖金')
    hourlyrate=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='小时工资率(HourlyRate)')
    compensate=models.IntegerField(verbose_name='等级激励(￥)',help_text='达到激励起点后才开始计算绩效奖金')
    incentivestr=models.DecimalField(max_digits=8, decimal_places=4,verbose_name='激励强度(￥)',help_text='扣除等级奖金后，超产每小时还需要分给人员奖金')
    incentivedist=models.DecimalField(max_digits=8, decimal_places=4,verbose_name='激励分配比(%)',help_text='超产部份按时薪比例分配奖金给人员，计算公式=(激励强度+单位等级激励)/时薪')
    dayhours=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='日工时数(时/天/人)')
    monthdays=models.IntegerField(verbose_name='月工作天数(天/月/人)')
    basesalary=models.IntegerField(verbose_name='基本底薪(￥)')
    revision=models.CharField(max_length=40,verbose_name='方案版本')
    states=models.BooleanField(default=1,verbose_name='有效')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%d-%s' %(self.SLP,self.level,self.revision)

    class Meta:
        verbose_name = '305SLP框架'
        verbose_name_plural = '305SLP框架'
        ordering = ['SLP','level','revision']
        unique_together=('SLP','level','revision')

#KPI方案
class KPI(models.Model):
    KPI = models.CharField(max_length=40,unique=True,verbose_name='KPI方案')
    kpidesc = models.TextField(null=True,blank=True,verbose_name='方案说明')    
    releasedate = models.DateField(default=timezone.now, verbose_name='生效日期')
    kpiindex = models.ManyToManyField('index',null=True,blank=True,verbose_name='KPI考核项目')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.KPI

    class Meta:
        verbose_name = '306KPI方案'
        verbose_name_plural = '306KPI方案'

#KPI项目
class index(models.Model):
    kpj=(
    ('Less',u'取小'),
    ('More',u'取大')  
    ) 
    KPI=models.CharField(max_length=40,verbose_name='KPI方案')
    kcode=models.CharField(max_length=40,verbose_name='KPI项目')
    Kdescription=models.CharField(max_length=120,verbose_name='KPI说明')
    kmax=models.DecimalField(max_digits=8, default=100,decimal_places=2,verbose_name='最大分')
    kmin=models.DecimalField(max_digits=8, default=-100,decimal_places=2,verbose_name='最小分')
    kbase=models.DecimalField(max_digits=8, default=0,decimal_places=2,verbose_name='基础分')
    kcriteria=models.DecimalField(max_digits=8,default=-10, decimal_places=2,verbose_name='计分值')
    kgrade=models.DecimalField(max_digits=8,default=0, decimal_places=2,verbose_name='目标值')    
    kjudge=models.CharField(max_length=10,default='More',choices=kpj,verbose_name='取大或取小')
    revision=models.CharField(max_length=40,verbose_name='方案版本')
    states=models.BooleanField(default=1,verbose_name='有效')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%s-%s' %(self.KPI,self.Kdescription,self.revision)

    class Meta:
        verbose_name = '307KPI项目'
        verbose_name_plural = '307KPI项目'
        ordering = ['KPI','kcode','revision']
        unique_together=('KPI','kcode','revision')

#产出标准
class ST(models.Model):
    item=models.CharField(max_length=60,verbose_name='项目')
    pcode=models.ForeignKey(pcode,on_delete=models.DO_NOTHING,verbose_name='制程')
    labor=models.DecimalField(max_digits=8,decimal_places=0,verbose_name='标准工时(单位：秒)')
    enable=models.DateField(default=timezone.now,verbose_name='生效日期')
    deadline=models.DateField(null=True,blank=True,verbose_name='失效日期',help_text='在此日期后标准将失效')
    revise=models.DecimalField(default=100,max_digits=8,decimal_places=2,verbose_name='标准修正比%)',help_text='值大于100，则按IE标准再加宽放计算绩效')
    port=models.BooleanField(default=1,verbose_name='按头数计算') 
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '308产出标准'
        verbose_name_plural = '308产出标准'
        ordering = ['item','pcode','enable',]
        unique_together=('item','pcode','enable')  

#考核期
class SLGMaster(models.Model):
    ye=(
    ('2017',u'2017年'),
    ('2018',u'2018年'),
    ('2019',u'2019年'),
    ('2020',u'2020年'),
    ('2021',u'2021年')  
    )
    mo=(
    ('1',u'1月'),
    ('2',u'2月'),
    ('3',u'3月'),
    ('4',u'4月'),
    ('5',u'5月'),
    ('6',u'6月'),
    ('7',u'7月'),
    ('8',u'8月'),
    ('9',u'9月'),
    ('10',u'10月'),
    ('11',u'11月'),
    ('12',u'12月')
    )
    dep=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'P'},related_name='plmaster',verbose_name='部门')
    YEA=models.CharField(max_length=10,choices=ye,default=datetime.datetime.now().year,verbose_name='年份')
    MON=models.CharField(max_length=10,choices=mo,default=datetime.datetime.now().month,verbose_name='月份') 
    states=models.BooleanField(default=1,verbose_name='有效',help_text='是否准许更新本期人员绩效考核有关数据')  
    AXD=models.ManyToManyField(axisdate,null=True,blank=True,verbose_name='考核日期')       
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%s-%s' %(self.dep,self.YEA,self.MON)

    class Meta:
        verbose_name = '309考核周期'
        verbose_name_plural = '309考核周期'
        ordering = ['YEA','MON','dep',]
        unique_together=('dep','YEA','MON')   


#闲置代码
class idlecode(models.Model):
    cate=(
    ('1',u'材料问题'),
    ('2',u'设备问题'),
    ('3',u'品质问题'),
    ('4',u'良率问题'),
    ('5',u'人员问题'),
    ('6',u'计划问题'),
    ('0',u'其它问题')   
    )    
    code=models.CharField(max_length=40,primary_key=True,verbose_name='闲置代码')
    category=models.CharField(max_length=40,choices=cate,verbose_name='闲置分类')
    responder=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='Responderuser',verbose_name='回应者',help_text='选择人员后，发生此项异常时，系统自动通知回应者')
    idledesc=models.TextField(null=True,verbose_name='闲置说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return '%s-%s-%s' %(self.code,self.idledesc,self.responder)

    class Meta:
        verbose_name = '310闲置代码'
        verbose_name_plural = '310闲置代码'
        ordering = ['category','code']



#出勤工时
class workinghour(models.Model):
    date=models.DateField(default=timezone.now,verbose_name='出勤日期')
    group=models.ForeignKey('group',on_delete=models.DO_NOTHING,related_name='orggroupwk',verbose_name='绩效群组')
    jn=models.ForeignKey('org',on_delete=models.DO_NOTHING,related_name='orgjnwk',verbose_name='人员工号')
    workinghours=models.DecimalField(max_digits=8,decimal_places=2, default=660.00,verbose_name='出勤工时(单位：分钟)')
    ADM=models.CharField(max_length=120,null=True,blank=True,verbose_name='说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '311出勤工时'
        verbose_name_plural = '311出勤工时'
        ordering = ['date','group','jn',]
        unique_together=('date','group','jn')  
 

#闲置工时
class idlehour(models.Model):
    date=models.DateField(default=timezone.now,verbose_name='工作日期')
    group=models.ForeignKey('group',on_delete=models.DO_NOTHING,related_name='groupid',verbose_name='绩效群组')
    jn=models.ForeignKey('org',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='idleorg',verbose_name='人员工号',help_text='若不需要细分，人员可以不记录')
    idlecode=models.ForeignKey('idlecode',on_delete=models.DO_NOTHING,max_length=40,verbose_name='闲置代码')
    idlehours=models.DecimalField(max_digits=8,decimal_places=2, default=0,verbose_name='闲置工时(单位：分钟)') 
    idledesc=models.TextField(null=True,blank=True,verbose_name='说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '312闲置工时'
        verbose_name_plural = '312闲置工时'
        ordering = ['date','group','jn','idlecode']
        unique_together=('date','group','jn','idlecode')  


#人员产出
class output(models.Model):
    date=models.DateField(default=timezone.now,verbose_name='工作日')
    dep=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'P'},related_name='rcppl',verbose_name='部门')
    cell=models.ForeignKey(department,on_delete=models.DO_NOTHING,limit_choices_to={'category':'C'},related_name='rcpcell',verbose_name='Cell')
    group=models.ForeignKey('group',on_delete=models.DO_NOTHING,related_name='rcpgroup',verbose_name='绩效群组')
    jn=models.ForeignKey('org',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='rcptor',verbose_name='人员工号')
    item=models.CharField(max_length=60,verbose_name='完工项目',help_text='输入料号或料号群码')
    pcode=models.CharField(max_length=60,verbose_name='完工制程',help_text='输入工作制程')
    qty=models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name='完工数量') 
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '313人员产出'
        verbose_name_plural = '313人员产出'
        ordering = ['date','dep','cell','group']
        unique_together=('date','item','pcode','group','jn')  

#目标调整
class correction(models.Model):
    date=models.DateField(default=timezone.now,verbose_name='工作日')
    group=models.ForeignKey('group',on_delete=models.DO_NOTHING,related_name='corgroupg',verbose_name='绩效群组')
    jn=models.ForeignKey('org',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='corjnorg',verbose_name='人员工号')
    checking=models.BooleanField(default=1,verbose_name='有效计算',help_text='有效表示当日按实际效率计算绩效，否则按100%计算绩效。')
    target=models.DecimalField(max_digits=8,decimal_places=4,null=True,blank=True,default=100,verbose_name='目标调整%',help_text='若有效计算，并重新按%设定新目标计算。') 
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '314目标调整'
        verbose_name_plural = '314目标调整'
        ordering = ['date','group','jn']
        unique_together=('date','group','jn')  

#KPI
class perkpi(models.Model):
    date=models.DateField(default=timezone.now,verbose_name='工作日')
    group=models.ForeignKey('group',on_delete=models.DO_NOTHING,related_name='pkpigg',verbose_name='绩效群组')
    jn=models.ForeignKey('org',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='pkpijng',verbose_name='人员工号')
    kpi=models.ForeignKey('index',on_delete=models.DO_NOTHING,limit_choices_to={'states':1},verbose_name='KPI')
    amount=models.DecimalField(max_digits=8,decimal_places=4,null=True,verbose_name='KPI量化数值') 
    pertext=models.TextField(null=True,blank=True,verbose_name='说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = '315KPI量化'
        verbose_name_plural = '315KPI量化'
        ordering = ['date','group','jn']
        unique_together=('date','group','jn')  


class projectitem(models.Model):
    cate=(
    ('1',u'1.启动'),
    ('2',u'2.规划'),
    ('3',u'3.实施'),
    ('4',u'4.监控'),
    ('5',u'5.收尾'),
    ('9',u'关闭'),
    ('0',u'取消'),
    )
    gory=(
    ('1',u'1.系统集成'),
    ('2',u'2.流程再造'),
    ('3',u'3.任务执行'),
    ('4',u'4.新产品开发'),
    ('5',u'5.现场改造'),
    ('6',u'6.制程改进'),
    ('0',u'0.其它'),
    )      
    ProjectCode=models.CharField(primary_key=True,max_length=20,verbose_name='编码')
    ProjectItem=models.CharField(max_length=120,verbose_name='名称')
    category=models.CharField(max_length=20,default='3',choices=gory,verbose_name='分类')
    ProjectTarget=models.TextField(null=True,blank=True,verbose_name='目标')
    ProjectValue=models.TextField(null=True,blank=True,verbose_name='效益')
    ProjectLeader=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='ProjectLeader',verbose_name='负责')
    ProjectMember=models.ManyToManyField(User,null=True,blank=True,related_name='ProjectMember',verbose_name='成员')
    StartDate=models.DateField(default=timezone.now,null=True,blank=True,verbose_name='启动日期')
    EndDate=models.DateField(null=True,blank=True,verbose_name='结案日期')
    ProjectVersion=models.CharField(max_length=20,default='A01',verbose_name='版本')
    States=models.CharField(max_length=40,default='1',choices=cate,verbose_name='状态')
    ParentCode=models.ForeignKey('self',null=True,blank=True,on_delete=models.DO_NOTHING,related_name='parentcode',verbose_name='来源')
    Dep=models.ManyToManyField(department,related_name='projectitem',null=True,blank=True,verbose_name='范围') 
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    def __str__(self):
        return self.ProjectCode

    class Meta:
        verbose_name = '316项目管理'
        verbose_name_plural = '316项目管理'


class projectRev(models.Model):
    ProjectCode=models.CharField(max_length=20,verbose_name='编码')
    ProjectItem=models.CharField(max_length=120,verbose_name='名称')
    ProjectTarget=models.TextField(null=True,blank=True,verbose_name='目标')
    ProjectValue=models.TextField(null=True,blank=True,verbose_name='效益评估')
    EndDate=models.DateField(default=timezone.now,null=True,blank=True,verbose_name='结案日期')
    ProjectVersion=models.CharField(max_length=20,default='A01',verbose_name='版本')
    States=models.CharField(max_length=40,verbose_name='项目状态')
    Remark=models.TextField(null=True,blank=True,verbose_name='项目阶段说明')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='修订时间')

    def __str__(self):
        return self.ProjectCode

    class Meta:
        verbose_name = '317项目记录'
        verbose_name_plural = '317项目记录'
        unique_together=('ProjectCode','ProjectVersion') 


class projectManage(models.Model):
    ProjectCode=models.OneToOneField('projectitem',on_delete=models.CASCADE,primary_key=True,verbose_name='项目')
    dim1=models.SmallIntegerField(default='0',verbose_name='重要性',help_text='0-2, 与公司/部门目标无相关性：0，与公司/部门目标间接相关：1，与公司/部门目标有直接相关：2。')
    dim2=models.SmallIntegerField(default='0',verbose_name='影响范围',help_text='0-2, 影响个人：0，部门内影响：1，跨部门影响：2。')
    dim3=models.SmallIntegerField(default='0',verbose_name='实施方法',help_text='0-1, 有SOP:0，无SOP首次进行的工作：1。')
    dim4=models.SmallIntegerField(default='0',verbose_name='标准化',help_text='0-2, 无任何标准化动作：0，只有部份规范文件：1，输出SOP文件并对人员培训等：2。')
    dim5=models.SmallIntegerField(default='0',verbose_name='时效性',help_text='0-2, 未完成：0，延迟完成：1，按时完成：2。')
    dim6=models.SmallIntegerField(default='0',verbose_name='报告记录',help_text='0-1,无报告无数据记录：0，有报告有数据记录：1。')
    dim7=models.SmallIntegerField(default='0',verbose_name='总评分',help_text='评分计算 = 困难度(重要性+影响范围+实施方法) X 成效度(标准化+时效性+报告记录) ')
    updatetime=models.DateTimeField(default=timezone.now,verbose_name='修订时间')

    def __str__(self):
        return self.ProjectCode

    class Meta:
        verbose_name = '318项目评价'
        verbose_name_plural = '318项目评价' 
