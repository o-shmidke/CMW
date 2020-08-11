from django import forms
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
