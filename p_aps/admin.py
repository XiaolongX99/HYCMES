# -*- coding:utf-8 -*-
from django.contrib import admin
from p_aps.models import *


@admin.register(demand)
class demandAdmin(admin.ModelAdmin):
	list_filter=['customerid','states',]
	search_fields = ["po",'item','podate','demanddate']
	list_display =['po','poid','item','itemdesc','itemspec','demandqty','demanddate']


@admin.register(mps)
class mpsAdmin(admin.ModelAdmin):
	list_filter=['dep','cell','states',]
	search_fields = ['po','item','poid','pdate']
	list_display =['po','poid','item','pdate','pqty','dep','cell']


@admin.register(shipment)
class shipmentAdmin(admin.ModelAdmin):
	list_filter=['status']
	search_fields = ['item','shippingdate','po','customer']
	list_display =['item','shippingdate','customer','po','poid','spec','qty','shippingtime','confirm','status']


@admin.register(packinglist)
class packinglistAdmin(admin.ModelAdmin):
	search_fields = ['item','packingdate','po','customer']
	list_display =['item','packingdate','customer','po','poid','spec','qty','packingmethod','boxsize','netweight','weight']


@admin.register(packing)
class packingAdmin(admin.ModelAdmin):
	search_fields = ['item','po','pn']
	list_display =['item','po','poid','box','boxid','pn','qty']


