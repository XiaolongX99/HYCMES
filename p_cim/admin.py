from django.contrib import admin
from p_cim.models import TemplateSN


#组织部门
@admin.register(TemplateSN)
class departmentAdmin(admin.ModelAdmin):
    list_filter= ["template"]
    search_fields = ["template", "item"]
    list_display =["template", "item",'Xaxis','Yaxis']