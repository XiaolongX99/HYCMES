# -*- coding:utf-8 -*-
from django.contrib import admin
from p_mes.models import deptarget


@admin.register(deptarget)
class deptargetAdmin(admin.ModelAdmin):
	list_filter=["dep"]
	search_fields = ["dep",'tcode']
	list_display =['tcode','dep','tvalue','tucl','tlcl']
	readonly_fields = ("updatename", )

	def save_model(self, request, obj, form, change):
		if not change:
			obj.updatename = request.user
		obj.save() 