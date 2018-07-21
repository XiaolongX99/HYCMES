from django.contrib import admin
from p_pdm.models import *
#PDM admin

#产品族
@admin.register(productgroup)
class productgroupAdmin(admin.ModelAdmin):
	search_fields = ["groupname"]
	list_display =['groupname','groupcode','PM']


#产品树
@admin.register(producttree)
class producttreeAdmin(admin.ModelAdmin):
	list_filter = ["PG","parent"]
	search_fields = ["productcode",'productname', "PDE"]
	list_display =['productname','productcode','parent','PDE','PG']
	filter_horizontal=('operation','process','item')



class itempcodeInline(admin.StackedInline):
    model = itempcode
    fieldsets = (
              (None, {'fields':(('step','pcode', 'updatename'), )}),
              )

#品号
@admin.register(item)
class itemAdmin(admin.ModelAdmin):
	list_filter = ["productgroup","states"]
	search_fields = ["item"]
	list_display =['item','itemdesc','itemspec','productgroup','itemgroup']
	inlines = [itempcodeInline,]



#产品线
@admin.register(productline)
class productlineAdmin(admin.ModelAdmin):
	search_fields = ["PL",'ERP','SFM','PDM','OPM','APS','SCM','WMS','ADM','MES']
	list_display =['PL','ERP','SFM','PDM','OPM','APS','SCM','WMS','ADM','MES']
	filter_horizontal=('operation',)


#工作中心
@admin.register(operation)
class operationAdmin(admin.ModelAdmin):
	list_filter = ["category",'parent']
	search_fields = ["opcode",'opname']
	list_display =['opcode','opname','parent','PCE','category']
	filter_horizontal=('process',)


#工作参数
@admin.register(process)
class processAdmin(admin.ModelAdmin):
	search_fields = ["process",]
	list_display =['process','prodesc','updatetime']


#作业制程
@admin.register(pcode)
class pcodeAdmin(admin.ModelAdmin):
	list_filter = ["operation",]
	search_fields = ["pname", "pcode"]
	list_display =['pname','pcode','labor','operation']

	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	
	

#修订记录
@admin.register(pcoderev)
class  pcoderevAdmin(admin.ModelAdmin):
	list_filter = ['pcode','states']
	search_fields = ['pcode','pname','changes','states']
	list_display =['pname','pcode','labor','changes','states']
	readonly_fields = ['pcode','pname','labor','states','updatename']

	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	


class ParameterInline(admin.StackedInline):
    model = itempcodespec
    fieldsets = (
              (None, {'fields':(('parameter', 'spec'),('UCL', 'CL','LCL'))}),
              )


#产品流程
@admin.register(itempcode)
class itempcodeAdmin(admin.ModelAdmin):
	list_filter = ["item",'pcode']
	search_fields = ["item__item",'pcode__pcode']
	list_display =['item','pcode','step']
	readonly_fields = ("updatename", )
	inlines = [ParameterInline,]

	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	


#制程参数
@admin.register(parameter)
class parameterAdmin(admin.ModelAdmin):
	list_filter = ["pmproperty","process"]
	search_fields = ["parameter",'spec']
	list_display =['parameter','spec','process',"pmproperty"]


#制程规格
@admin.register(itempcodespec)
class itempcodespecAdmin(admin.ModelAdmin):
	search_fields = ['parameter__parameter','spec']
	list_display =['route','parameter','spec','UCL','CL','LCL']
	readonly_fields = ("updatename", )


	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	



#BOM-Port
@admin.register(bomport)
class bomportAdmin(admin.ModelAdmin):
	search_fields = ["item"]
	list_display =['item','port','updatetime']

#BOM
@admin.register(itembom)
class itembomAdmin(admin.ModelAdmin):
	search_fields = ["item",'component']
	list_display =['item','seq','component','qty','loss','units','starttime','endtime']