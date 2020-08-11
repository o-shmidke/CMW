from django.urls import path, include

# from CMW.utils import document_download
from .views import home, object_create_view, ObjectUpdateView, ObjectDeleteView, detail, documents_view, \
    documents_upload, documents_delete

from CMW.urls import *

app_name = 'object'
urlpatterns = [

    path('<str:slug_proj>/objects/add/', object_create_view, name="add"),
    path('<str:slug_proj>/objects/update/<str:slug>/', ObjectUpdateView.as_view(), name="update"),
    path('<str:slug_proj>/objects/delete/<str:slug>/', ObjectDeleteView.as_view(), name="delete"),
    path('<str:slug_proj>/objects/detail/<str:slug>/', detail, name="detail"),
    path('<str:slug_proj>/objects/', home, name="home"),
    path('<str:slug_proj>/objects/<str:slug>/documents_view/', documents_view, name="documents_view"),
    path('<str:slug_proj>/objects/<str:slug>/documents_upload/', documents_upload, name="documents_upload"),
    path('<str:slug_proj>/objects/<str:slug>/documents_delete/<int:pk>', documents_delete, name="documents_delete"),


    # path('<str:slug_proj>/objects/<str:slug>/documents_download_all/', getfiles, name="documents_download_all"),
    # path('objects/document_download/<path>/', document_download, name="document_download"),

    path('<str:slug_proj>/objects/<str:slug>/materials/', include('materials.urls', 'materials'),
         name='materials_view'),
]
