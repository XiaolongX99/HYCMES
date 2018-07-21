# -*- coding:utf-8 -*-
from django.contrib import admin
from p_opm.models import *

# OPM admin

@admin.register(org)
class orgAdmin(admin.ModelAdmin):
	list_filter=['cell','operation','states']
	search_fields = ["jn",'cell','group','operation']
	list_display =["jn",'cell','group','operation']
	filter_horizontal=('skill',)


@admin.register(skill)
class cellsAdmin(admin.ModelAdmin):
	list_filter=["skillcode",'nvalue','states']
	search_fields = ['skillcode','skilldesc','kvalue','nvalue']
	list_display =['skillcode','skilldesc','kvalue','nvalue','allowance']
	filter_horizontal=('operation',)


@admin.register(group)
class groupadmin(admin.ModelAdmin):
	list_filter=["groupcode",'AMT','SLP','KPI']
	search_fields = ["groupcode",'AMT','SLP','KPI']
	list_display =['groupcode','groupdesc','AMT','SLP','KPI','updatetime']
	filter_horizontal=('jn','cell')


@admin.register(SLG)
class SLGAdmin(admin.ModelAdmin):
	list_filter=["SLP",]
	search_fields = ["SLP",'releasedate','slpdesc']
	list_display =['SLP','slpdesc','releasedate',]
	filter_horizontal=('frame',)


@admin.register(SLGFrame)
class SLGFrameAdmin(admin.ModelAdmin):
	list_filter=["SLP",'revision','states']
	search_fields = ["SLP",'level','revision',]
	list_display =['level','UPPH','Grade','compensate','incentivestr','hourlyrate','incentivedist',]


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
	list_filter=["KPI"]
	search_fields = ["KPI",'releasedate','kpidesc']
	list_display =['KPI','kpidesc','releasedate',]
	filter_horizontal=('kpiindex',)


@admin.register(index)
class indexAdmin(admin.ModelAdmin):
	list_filter=["KPI",'revision','states']
	search_fields = ["KPI",'kcode','revision',]
	list_display =['kcode','Kdescription','kmax','kmin','kbase','kcriteria','kgrade','kjudge','revision']


@admin.register(ST)
class STAdmin(admin.ModelAdmin):
	list_filter=['port']
	search_fields = ['item','pcode','revise','enable','deadline']
	list_display =['item','pcode','enable','deadline','revise','labor','port']


@admin.register(SLGMaster)
class SLGMasterAdmin(admin.ModelAdmin):
	list_filter=["dep",'YEA','MON','states']
	search_fields = ["dep",'YEA','MON',]
	list_display =["dep",'YEA','MON','states','updatetime']
	filter_horizontal=('AXD',)


@admin.register(idlecode)
class idlecodeAdmin(admin.ModelAdmin):
	list_filter=["category",'responder']
	search_fields = ["code",'idledesc',]
	list_display =['code','category','idledesc','responder']


@admin.register(workinghour)
class workinghourAdmin(admin.ModelAdmin):
	list_filter=["date",'group','jn']
	search_fields = ["date",'group','jn',]
	list_display =["date",'group','jn','workinghours']


@admin.register(idlehour)
class idlehourAdmin(admin.ModelAdmin):
	list_filter=["group",'idlecode']
	search_fields = ["date",'idledesc','jn']
	list_display =['group','idlecode','idledesc','jn','idlehours']


@admin.register(output)
class outputAdmin(admin.ModelAdmin):
	list_filter=["group",'dep','cell']
	search_fields = ["date",'jn','pcode','item']
	list_display =['date','item','pcode','group','jn','qty','dep','cell']


@admin.register(correction)
class correctionAdmin(admin.ModelAdmin):
	list_filter=["group"]
	search_fields = ["date",'jn','group']
	list_display =['date','group','jn','checking','target']

@admin.register(perkpi)
class perkpiAdmin(admin.ModelAdmin):
	list_filter=["group",'kpi']
	search_fields = ["date",'group','jn','kpi']
	list_display =['date','group','jn','kpi','amount','pertext']

@admin.register(projectitem)
class projectitemadmin(admin.ModelAdmin):
	list_filter=["category",'States']
	search_fields = ["ProjectCode",'ProjectItem','ProjectLeader','StartDate','ProjectVersion']
	list_display =["ProjectCode",'ProjectItem','ProjectLeader','StartDate','EndDate','ProjectVersion','States']
	filter_horizontal=('ProjectMember','Dep')

@admin.register(projectRev)
class projectRevadmin(admin.ModelAdmin):
	list_filter=['States']
	search_fields = ["ProjectCode",'updatetime']
	list_display =["ProjectCode",'ProjectItem','EndDate','ProjectVersion','States','Remark']


@admin.register(projectManage)
class projectManageadmin(admin.ModelAdmin):
	search_fields = ["ProjectCode",'ProjectItem','EndDate','ProjectVersion']
	list_display =["ProjectCode",'dim1','dim2','dim3','dim4','dim5','dim6','dim7']