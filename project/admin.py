from django.contrib import admin
from project.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _


# class UserProfile(admin.ModelAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', "patronymic_name", "ID_Position", 'email', 'img')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     list_display = ('username', 'email', 'last_name', 'first_name', "patronymic_name", "ID_Position", 'is_staff')
#     filter_horizontal = ('groups', 'user_permissions',)


# admin.site.register(UserProfile)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Project)
admin.site.register(Position)

# @admin.register(CustomUser)
# class UserAdmin(admin.ModelAdmin):
#     add_form_template = 'admin/auth/user/add_form.html'
#     change_user_password_template = None
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', "patronymic_name", "ID_Position", 'email', 'img')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     list_display = ('username', 'email', 'first_name', 'last_name', "ID_Position", 'is_staff')
