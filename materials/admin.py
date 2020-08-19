from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from materials.models import *

admin.site.register(Materials)
admin.site.register(PlanMaterials)
admin.site.register(Groups)
#
#
# @admin.register(PlanMaterials)
# class PlanMaterialsAdmin(ImportExportModelAdmin):
#     list_display = ('material', 'quantity_plan', 'quantity_delivered', 'name_object')
