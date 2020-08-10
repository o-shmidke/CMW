import datetime

from django import forms
from django.contrib.admin import widgets
from project.models import Project, CustomUser
from .models import *
from .views import *


class PlanWorksForm(forms.ModelForm):
    type_works = forms.ModelChoiceField(label='Наименование работы',
                                        queryset=TypeOfWork.objects.all(),
                                        widget=forms.Select(
                                            attrs={'class': "form-control js-example-basic-single",
                                                   }))

    quantity_plan = forms.DecimalField(label='Планируемое колличество', widget=forms.NumberInput(
        attrs={'class': "form-control",
               'placeholder': 'Кол-во работ'}))
    comment = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={'class': "form-control",
                                                                                               'placeholder': 'Доп.информация',
                                                                                               'style': 'height: 150px'}))

    class Meta(object):
        model = PlanWorks
        fields = (
            'type_works', 'quantity_plan', 'comment')

    def __init__(self, slug=None, *args, **kwargs):
        super(PlanWorksForm, self).__init__(*args, **kwargs)

    def clean_type_works(self):
        a = self.cleaned_data['type_works']

        if not a:
            raise forms.ValidationError('Необходимо выбрать один из пунктов')
        return a

    def clean_quantity_plan(self):
        a = self.cleaned_data['quantity_plan']
        if not a:
            raise forms.ValidationError('Необходимо заполнить поле')
        return a


class CompleteWorksForm(forms.ModelForm):
    type_works = forms.ModelChoiceField(label='Наименование работы',
                                        queryset=TypeOfWork.objects.all(),
                                        widget=forms.Select(
                                            attrs={'class': "form-control js-example-basic-single",
                                                    'id':'type_works_input'
                                                   }))

    quantity_complete = forms.DecimalField(label='Выполнено (кол-во)', widget=forms.NumberInput(
        attrs={'class': "form-control js-example-basic-single",
               'placeholder': 'Введите кол-во выполненных работ'}))

    date = forms.DateField(label='Дата выполнения', input_formats=['%d.%m.%Y'],
                           widget=forms.DateInput(attrs={'class': "form-control datepicker ", 'id': 'datetimepicker2',
                                                         'placeholder': 'Дата'})
                           )
    comment = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={'class': "form-control",
                                                                                               'placeholder': 'Доп.информация',
                                                                                               'style':'height: 80px'}))

    class Meta(object):
        model = CompleteWorks
        fields = (
            'type_works',
            'quantity_complete', 'date', 'comment')

    def __init__(self, slug=None, *args, **kwargs):
        super(CompleteWorksForm, self).__init__(*args, **kwargs)
        # self.fields['type_works'].queryset = TypeOfWork.objects.filter(planworks__name_object__slug__iexact=slug)

    def clean_type_works(self):
        a = self.cleaned_data['type_works']

        if not a:
            raise forms.ValidationError('Необходимо выбрать один из пунктов')
        return a

    def clean_quantity_plan(self):
        a = self.cleaned_data['quantity_plan']
        if not a:
            raise forms.ValidationError('Необходимо заполнить поле')
        return a


class SearchWorksForm(forms.ModelForm):
    q = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': "form-control ", 'placeholder': 'Поиск '}))
    slug_o = forms.CharField(label=False, required=True, widget=forms.TextInput(
        attrs={'class': "form-control "}))
    slug_p = forms.CharField(label=False, required=True, widget=forms.TextInput(
        attrs={'class': "form-control "}))

    class Meta(object):
        model = PlanWorks
        fields = ('q', 'slug_o', 'slug_p')

    # def __init__(self, slug=None, *args, **kwargs):
    #     super(SearchWorksForm, self).__init__(*args, **kwargs)
    # self.fields['type_works'].queryset = TypeOfWork.objects.filter(planworks__name_object__slug__iexact=slug)


class CheckCompleteWorksForm(forms.ModelForm):
    type_works = forms.ModelChoiceField(label='Наименование работы',
                                        queryset=TypeOfWork.objects.all(),
                                        widget=forms.Select(
                                            attrs={'class': "form-control js-example-basic-single",
                                                   'id': 'type_works_check',
                                                   }))
    slug_o = forms.CharField(label=False, required=True, widget=forms.TextInput(
        attrs={'class': "form-control "}))
    slug_p = forms.CharField(label=False, required=True, widget=forms.TextInput(
        attrs={'class': "form-control "}))

    class Meta(object):
        model = CompleteWorks
        fields = (
            'type_works', 'slug_o', 'slug_p')

    def __init__(self, slug=None, *args, **kwargs):
        super(CheckCompleteWorksForm, self).__init__(*args, **kwargs)
        self.fields['type_works'].queryset = TypeOfWork.objects.filter(planworks__name_object__slug__iexact=slug)
