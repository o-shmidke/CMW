from django import forms

from .models import *
from .views import *


class PlanMaterialsForm(forms.ModelForm):
    material = forms.ModelChoiceField(label='Наименование',
                                      queryset=Materials.objects.all(),
                                      widget=forms.Select(
                                          attrs={'class': "form-control js-example-basic-single",
                                                 'id': 'change_material'
                                                 }))
    quantity_plan = forms.DecimalField(label='Планируемое колличество', widget=forms.NumberInput(
        attrs={'class': "form-control", 'placeholder': 'Кол-во'}))
    quantity_delivered = forms.DecimalField(label='Поставленное колличество', widget=forms.NumberInput(
        attrs={'class': "form-control", 'placeholder': 'Кол-во', 'value': 0}))

    class Meta(object):
        model = PlanMaterials
        fields = (
             'material', 'quantity_plan', 'quantity_delivered')

    def __init__(self, slug=None, *args, **kwargs):
        super(PlanMaterialsForm, self).__init__(*args, **kwargs)


class SearchPlanMaterialsForm(forms.ModelForm):
    q = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': "form-control ", 'placeholder': 'Поиск '}))
    slug_o = forms.CharField(label=False, required=True, widget=forms.TextInput(
        attrs={'class': "form-control ", }))

    class Meta(object):
        model = PlanMaterials
        fields = ('q', 'slug_o')

    #
    # def __init__(self, , *args, **kwargs):
    #     self.fields['slug_o'].queryset = Object.objects.get(slug__iexact=request.slug)
    #     super(SearchPlanMaterialsForm, self).__init__(*args, **kwargs)


# class UpdatePlanMaterialsForm(forms.ModelForm):
#     group = forms.ModelChoiceField(label='Группа',
#                                    queryset=Groups.objects.all(),
#                                    widget=forms.Select(
#                                        attrs={'class': "form-control js-example-basic-single",
#                                               }))
#     slug_o = forms.CharField(label=False, required=True, widget=forms.TextInput(
#         attrs={'class': "form-control ", }))
#
#     class Meta(object):
#         model = PlanMaterials
#         fields = ('group','slug_o')
