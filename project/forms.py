from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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





class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
