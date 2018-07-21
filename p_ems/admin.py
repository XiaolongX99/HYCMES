# -*- coding:utf-8 -*-
from django.contrib import admin
from p_ems.models import *


@admin.register(assets)
class assetsAdmin(admin.ModelAdmin):
	list_filter=['assets','supply']
	search_fields = ["scode",'sname','sspec','category']
	list_display =["scode",'sname','sspec','category','parent','assets','supply','entrydate']


@admin.register(equipment)
class equipmentAdmin(admin.ModelAdmin):
	list_filter=['status','MEG']
	search_fields = ['ecode','ename','station']
	list_display =['ecode','ename','status','station','MEG','remark']

	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	


@admin.register(station)
class stationAdmin(admin.ModelAdmin):
	list_filter=['dep']
	search_fields = ['cell','operation','PIC']
	list_display =['station','dep','cell','operation','PIC','stationdesc']


@admin.register(tpmitem)
class tpmitemAdmin(admin.ModelAdmin):
	list_filter=['category']
	search_fields = ['mcode','mitem','mspec']
	list_display =['mcode','mitem','mspec','category','period']


@admin.register(runstatus)
class runstatusAdmin(admin.ModelAdmin):
	list_filter=['status']
	search_fields = ['equipment','station']
	list_display =['equipment','status','station','starttime','endtime']

	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	

@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
	search_fields = ['tcode','tname','tdesc']
	list_display =['tcode','tname','tdesc','parent','userguide']
	filter_horizontal=('tpm','equipment')


@admin.register(tpmrecords)
class tpmrecordsAdmin(admin.ModelAdmin):
	list_filter=['judge']
	search_fields = ['tpmdate','equipment','item']
	list_display =['tpmdate','equipment','item','judge','remark']

	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	


@admin.register(troublecode)
class troublecodeAdmin(admin.ModelAdmin):
	list_filter=['PIC']
	search_fields = ['troublecode','troublename']
	list_display =['troublecode','troublename','PIC']


@admin.register(troublerecords)
class troublerecordsAdmin(admin.ModelAdmin):
	list_filter=['dispose','status']
	search_fields = ['equipment','trouble','createname','confirm']
	list_display =['equipment','trouble','createname','confirm','dispose','status']