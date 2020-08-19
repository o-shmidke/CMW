from django import forms

from .views import *


class PlanMaterialsForm(forms.ModelForm):
    material = forms.ModelChoiceField(label='Наименование',
                                      queryset=Materials.objects.all(),
                                      widget=forms.Select(
                                          attrs={'class': "form-control js-example-basic-single",
                                                 'id': 'change_material'
                                                 }))
    # group = forms.ModelChoiceField(label='Группа',
    #                                queryset=Groups.objects.all(),
    #                                widget=forms.Select(
    #                                    attrs={'class': "form-control js-example-basic-single", 'id': 'change_group'
    #                                           }))
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
        # self.fields['type_works'].queryset = Materials.objects.filter(planworks__name_object__slug__iexact=slug)

    # def clean_type_works(self):
    #     a = self.cleaned_data['type_works']
    #
    #     if not a:
    #         raise forms.ValidationError('Необходимо выбрать один из пунктов')
    #     return a
    #
    # def clean_quantity_plan(self):
    #     a = self.cleaned_data['quantity_plan']
    #     if not a:
    #         raise forms.ValidationError('Необходимо заполнить поле')
    #     return a


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
