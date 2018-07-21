from django.contrib import admin
from p_scm.models import rfqgroup
#SCM admin

@admin.register(rfqgroup)
class productgroupAdmin(admin.ModelAdmin):
	search_fields = ["category"]
	list_display =['category','group','groupvalue']
