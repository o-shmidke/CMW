from django.urls import path, include
from .views import *

app_name = 'project'

urlpatterns = [
    path('', home, name="home"),
    path('upload_photo/', upload_photo, name="upload_photo"),
]
