from django.contrib import admin
from project.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Project)
admin.site.register(Position)
