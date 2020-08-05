from django.urls import path, include
from .views import view_plan_materials, export_plan_materials, create_plan_materials, delete_plan_materials, \
    update_plan_materials
from CMW.urls import *

app_name = 'materials'
urlpatterns = [

    path('plan/', view_plan_materials, name="plan_materials_view"),
    path('plan/create/', create_plan_materials, name="plan_materials_create"),
    path('plan/delete/<int:pk>', delete_plan_materials, name="plan_materials_delete"),
    path('plan/update/<int:pk>', update_plan_materials, name="plan_materials_update"),
    path('plan/download/', export_plan_materials,
         name="dowload_plan_materials"),

    # path('plan/search_plan_materials/', search_plan_materials, name="search_plan_materials"),
]
