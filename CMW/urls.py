"""CMW URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from materials.views import search_plan_materials
from work.views import search_plan_works, search_complete_works, check_complete_work

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls', "project"), name='project_view'),
    path('projects/detail/', include('object.urls', 'object'), name='object_view'),
    # path('objects/', include('object.urls')),
    path('project/', include('work.urls', 'work'), name="work_view"),
    path('accounts/', include('django.contrib.auth.urls')),

    path('search_plan_materials/', search_plan_materials, name="search_plan_materials"),
    path('search_plan_works/', search_plan_works, name="search_plan_works"),
    path('search_complete_works/', search_complete_works, name="search_complete_works"),
    # path('check_complete_works/', check_complete_work, name="check_complete_work"),
    # path('create_photo_form/', create_photo_form, name="create_photo_form"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
