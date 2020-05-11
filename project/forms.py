from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    name_project = forms.CharField(label='Наименование ГК', widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': 'Введите наименование ГК'}))
    perform_proc = forms.IntegerField(label='Выполнено', widget=forms.IntegerField(
        attrs={'class': "form-control",
               'placeholder': 'Выберите откуда следует поезд'}))

    class Meta(object):
        model = Project
        fields = ('name_project', 'perform_proc')
