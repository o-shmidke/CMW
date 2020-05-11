from django.urls import path, include
from .views import *

app_name = 'project'

urlpatterns = [
    path('', home, name="home"),

]
