from django.urls import path
from .views import *

app_name = 'work'
urlpatterns = [
    path('<str:slug_proj>/objects/detail/<str:slug>/work/plan/', plan_work_view, name="plan_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/plan/create/', plan_work_create, name="create_plan_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/plan/delete/<int:pk>', delete_plan_work,
         name="delete_plan_work"),
    # path('<str:slug_proj>/objects/<str:slug>/work/plan/update/<int:pk>', PlanWorksUpdateView.as_view(),
    #      name="update_plan_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/plan/update/<int:pk>', plan_work_update,
         name="update_plan_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/plan/download/', export_plan_work,
         name="dowload_plan_work"),


    path('<str:slug_proj>/objects/detail/<str:slug>/work/complete/', complete_work_view, name="complete_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/complete/create/', complete_work_create, name="create_complete_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/complete/delete/<int:pk>', CompleteWorksDeleteView.as_view(),
         name="delete_complete_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/complete/update/<int:pk>', complete_work_update,
         name="update_complete_work"),
    path('<str:slug_proj>/objects/<str:slug>/work/complete/download/', export_complete_work,
         name="dowload_complete_work"),
]
