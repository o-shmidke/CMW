from django import forms

from project.models import Project, CustomUser
from .models import Object
from .views import *


class ObjectForm(forms.ModelForm):
    Name_Object = forms.CharField(label='Наименование объекта', widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': 'Введите наименование объекта'}))
    Adress_Object = forms.CharField(label='Адрес', widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': 'Введите адрес объекта'}))
    NCH_General = forms.IntegerField(label='Общее кол-во нормочасов', widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': 'Введите общее кол-во нормочасов'}))
    ID_Rukovoditel = forms.ModelChoiceField(label='Руководитель', queryset=CustomUser.objects.filter(
        ID_Position__Name_Position='Руководитель'), widget=forms.Select(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Выберите руководителя объекта'}))
    ID_Menedger = forms.ModelChoiceField(label='Менеджер', queryset=CustomUser.objects.filter(
        ID_Position__Name_Position='Менеджер'), widget=forms.Select(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Выберите менеджера объекта'}))
    ID_Ingener = forms.ModelChoiceField(label='Инженер', queryset=CustomUser.objects.filter(
        ID_Position__Name_Position='Инженер'), widget=forms.Select(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Выберите инженера объекта'}))
    ID_Montazhnik = forms.ModelChoiceField(label='Старший монтажник', queryset=CustomUser.objects.filter(
        ID_Position__Name_Position='Монтажник'), widget=forms.Select(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Выберите монтажника объекта'}))

    class Meta(object):
        model = Object
        fields = (
            'Name_Object', 'Adress_Object', 'NCH_General', 'ID_Rukovoditel', 'ID_Menedger', 'ID_Ingener',
            'ID_Montazhnik')


