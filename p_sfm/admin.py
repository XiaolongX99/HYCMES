# -*- coding:utf-8 -*-
from django.contrib import admin
from p_sfm.models import *


@admin.register(dispatch)
class dispatchAdmin(admin.ModelAdmin):
	list_filter=['PL','cell','operation','states']
	search_fields = ["po",'wo','item','startdate']
	list_display =["po",'wo','item','startdate','startqty','completedate','completeqty']


@admin.register(transfer)
class transferAdmin(admin.ModelAdmin):
	list_filter=['PL','cell','operation','states']
	search_fields = ['po','wo','item','startdate']
	list_display =["po",'wo','item','groups','passqty','failqty','states']
	

@admin.register(transfertracking)
class trackingAdmin(admin.ModelAdmin):
	search_fields = ['lot','component',]
	list_display =["trid",'component','lot','failqty','faildesc']


@admin.register(modelfail)
class failmodelAdmin(admin.ModelAdmin):
	list_filter=['operation','product']
	search_fields = ['failcode','faildesc','responder']
	list_display =['failcode','faildesc','operation','product','responder']


@admin.register(transferfail)
class faildetailAdmin(admin.ModelAdmin):
	list_filter=['states']
	search_fields = ['sn','failcode','faildesc']
	list_display =['sn','failcode','failqty','faildesc','states']


@admin.register(modelqc)
class qcmodelAdmin(admin.ModelAdmin):
	list_filter=['operation','product']
	search_fields = ['qccode','qcdesc','responder']
	list_display =['qccode','qcdesc','operation','product','responder']


@admin.register(transferqc)
class fqcdetailAdmin(admin.ModelAdmin):
	list_filter=['qccode','result']
	search_fields = ['qccode','qcdesc']
	list_display =['trid','qccode','qcdesc','qcqty','failqty','result']


@admin.register(CELLHR)
class cellthAdmin(admin.ModelAdmin):
	list_filter=['PL','cell']
	search_fields = ['workingdate','PL','cell']
	list_display =['workingdate','PL','cell','members','workinghours']

