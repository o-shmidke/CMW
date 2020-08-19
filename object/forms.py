import re

from django import forms

from .models import Object, Documents
from .views import *

from django.forms import MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select


class PhoneWidget(MultiWidget):
    def __init__(self, code_length=3, num_length=7, attrs=None):
        widgets = [TextInput(attrs={
            'size': 10, 'maxlength': 10, 'value': "+7",
            'class': 'form-control is-invalid', }),
            # TextInput(attrs={'size': num_length, 'maxlength': num_length, })
        ]
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            code = ''
            num = ''
            sch = 0
            for i in value:
                if sch >= 2 and sch < 5:
                    code += value[sch]
                elif sch >= 5 and sch < 12:
                    num += value[sch]
                sch += 1
            return [code, num]
        else:
            return ['', '']

    def format_output(self, rendered_widgets):
        return '+7' + rendered_widgets[0]


class PhoneField(MultiValueField):

    def __init__(self, code_length=3, num_length=7, *args, **kwargs):
        list_fields = [CharField(),
                       # CharField()
                       ]
        super(PhoneField, self).__init__(list_fields, widget=PhoneWidget(code_length, num_length), *args, **kwargs)

    def compress(self, values):
        return '+7' + values[0]


class ObjectForm(forms.ModelForm):
    Name_Object = forms.CharField(label='Наименование объекта', required=False, widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': 'Введите наименование объекта'}))
    Adress_Object = forms.CharField(label='Адрес', required=False, widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': 'Введите адрес объекта'}))
    # NCH_General = forms.DecimalField(label='Общее кол-во нормочасов', required=False, widget=forms.TextInput(
    #     attrs={'class': "form-control",
    #            'placeholder': 'Введите общее кол-во нормочасов'}))
    # Number_phone = PhoneField(label='Номер телефона', required=False, )
    Number_phone = forms.CharField(label='Номер телефона', required=False, widget=forms.TextInput(
        attrs={'class': "form-control", 'size': 12, 'maxlength': 12, 'value': "+7",
               'placeholder': ''}))
    FIO_zakazchika = forms.CharField(label='ФИО заказчика', required=False, widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': 'Введите ФИО заказчика'}))
    Note = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(
        attrs={'class': "form-control",
               'placeholder': 'Доп.информация'}))
    ID_Rukovoditel = forms.ModelChoiceField(label='Руководитель', required=False, queryset=CustomUser.objects.filter(
        ID_Position__Name_Position='Руководитель'), widget=forms.Select(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Выберите руководителя объекта'}))
    ID_Menedger = forms.ModelChoiceField(label='Менеджер', required=False, queryset=CustomUser.objects.filter(
        ID_Position__Name_Position='Менеджер'), widget=forms.Select(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Выберите менеджера объекта'}))
    ID_Ingener = forms.ModelChoiceField(label='Инженер', required=False, queryset=CustomUser.objects.filter(
        ID_Position__Name_Position='Инженер'), widget=forms.Select(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Выберите инженера объекта'}))
    ID_Montazhnik = forms.ModelChoiceField(label='Старший монтажник', required=False,
                                           queryset=CustomUser.objects.filter(
                                               ID_Position__Name_Position='Бригадир'), widget=forms.Select(
            attrs={'class': "form-control js-example-basic-single",
                   'placeholder': 'Выберите монтажника объекта'}))

    def clean_slug(self):
        new_slug = self.cleaned_data['slug']

    def clean_Number_phone(self):
        a = self.cleaned_data['Number_phone']
        result = re.search(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', a)

        if not a:
            raise forms.ValidationError('Необходимо ввести номер телефона.')
        else:
            if not result:
                raise forms.ValidationError('Некорректно введен номер.')
        return a

    def clean_Name_Object(self):
        a = self.cleaned_data['Name_Object']
        if not a:
            raise forms.ValidationError('Необходимо заполнить поле.')

        return a

    def clean_Adress_Object(self):
        a = self.cleaned_data['Adress_Object']
        if not a:
            raise forms.ValidationError('Необходимо заполнить поле.')
        return a

    # def clean_NCH_General(self):
    #     a = self.cleaned_data['NCH_General']
    #     if not a:
    #         raise forms.ValidationError('Необходимо заполнить поле.')
    #     return a

    def clean_FIO_zakazchika(self):
        a = self.cleaned_data['FIO_zakazchika']
        if not a:
            raise forms.ValidationError('Необходимо заполнить поле.')
        return a

    # def clean_ID_Rukovoditel(self):
    #     a = self.cleaned_data['ID_Rukovoditel']
    #     if not a:
    #         raise forms.ValidationError('Необходимо заполнить поле.')
    #
    # def clean_ID_Menedger(self):
    #     a = self.cleaned_data['ID_Menedger']
    #     if not a:
    #         raise forms.ValidationError('Необходимо заполнить поле.')
    #
    # def clean_ID_Ingener(self):
    #     a = self.cleaned_data['ID_Ingener']
    #     if not a:
    #         raise forms.ValidationError('Необходимо заполнить поле.')
    #
    # def clean_ID_Montazhnik(self):
    #     a = self.cleaned_data['ID_Montazhnik']
    #     if not a:
    #         raise forms.ValidationError('Необходимо заполнить поле.')

    class Meta(object):
        model = Object
        fields = (
            'Name_Object', 'Adress_Object', 'Number_phone', 'FIO_zakazchika', 'ID_Rukovoditel',
            'ID_Menedger', 'ID_Ingener', 'ID_Montazhnik', "Note")


class DocumentsForm(forms.ModelForm):
    documents = forms.FileField(label='Документы', widget=forms.ClearableFileInput(attrs={'class': "form-control",
                                                                                          'multiple': True}))

    class Meta:
        model = Documents
        fields = ('documents',)


