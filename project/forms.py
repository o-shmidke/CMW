from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _

from .models import Project, CustomUser


# class ProjectForm(forms.ModelForm):
#     Name_Project = forms.CharField(label='Наименование ГК', widget=forms.TextInput(
#         attrs={'class': "form-control",
#                'placeholder': 'Введите наименование ГК'}))
#     Perform_proc = forms.IntegerField(label='Выполнено', widget=forms.TextInput(
#         attrs={'class': "form-control",
#                'placeholder': 'Выберите откуда следует поезд'}))
#
#     class Meta(object):
#         model = Project
#         fields = ('Name_Project', 'Perform_proc')


class CreatePhoto(forms.ModelForm):
    img = forms.ImageField(label='Фото', widget=forms.FileInput(attrs={'class': "form-control",
                                                                       }))

    class Meta:
        model = CustomUser
        fields = ('img',)

    # def get_form(self):/


class Auth(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': "form-control"}))

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': "form-control"}),
    )
