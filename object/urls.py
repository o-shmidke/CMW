from django.urls import path, include
from .views import home, object_create_view, ObjectUpdateView, ObjectDeleteView, detail
from CMW.urls import *

app_name = 'object'
urlpatterns = [

    path('<str:slug_proj>/objects/add/', object_create_view, name="add"),
    path('<str:slug_proj>/objects/update/<str:slug>/', ObjectUpdateView.as_view(), name="update"),
    path('<str:slug_proj>/objects/delete/<str:slug>/', ObjectDeleteView.as_view(), name="delete"),
    path('<str:slug_proj>/objects/detail/<str:slug>/', detail, name="detail"),
    path('<str:slug_proj>/objects/', home, name="home"),

    path('<str:slug_proj>/objects/<str:slug>/materials/', include('materials.urls', 'materials'), name='materials_view'),
]
