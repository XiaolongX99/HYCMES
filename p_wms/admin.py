from django.contrib import admin
from p_wms.models import warehouse,locator,transaction,storage,item

#仓库
@admin.register(warehouse)
class warehouseAdmin(admin.ModelAdmin):
	search_fields = ["code"]
	list_display =['code','name','FA','wmsdesc']

#储位
@admin.register(locator)
class locatorAdmin(admin.ModelAdmin):
	list_filter = ["parent",'states']
	search_fields = ["code",'name', "PDE"]
	list_display =['code','name','Xaxis','Yaxis','Zaxis','parent','states',]


#进出
@admin.register(transaction)
class transactionAdmin(admin.ModelAdmin):
	list_filter = ["IO",'warehouse']
	search_fields = ["locator",'item','lot']
	list_display =['IO','item','lot','warehouse','locator','qty','capacity','updatetime']
	readonly_fields = ("updatename", )
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save()	

#存货
@admin.register(storage)
class storageAdmin(admin.ModelAdmin):
	list_filter = ['warehouse']
	search_fields = ["locator",'item','lot']
	list_display =['item','lot','warehouse','locator','qty','capacity','updatetime']


#品号
@admin.register(item)
class itemAdmin(admin.ModelAdmin):
	list_filter = ['warehouse']
	search_fields = ['item','itemdesc']
	list_display =['item','itemdesc','uom','volume','weight','minqty','maxqty','lotcontrol','validity']
	filter_horizontal=('locator',)