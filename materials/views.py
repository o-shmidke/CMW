import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.template.loader import render_to_string

from CMW.resources import MaterialsResource, PlanMaterialsResource
from CMW.utils import export_xls

from materials.forms import PlanMaterialsForm, SearchPlanMaterialsForm
from .models import *

from tablib import Dataset


def upload_materials(request, slug_proj, slug):
    """Загрузка материалов из файла .xls"""
    if request.method == 'POST':
        materials_resource = MaterialsResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']
        imported_data = dataset.load(new_persons.read())
        materials_resource.import_data(dataset, dry_run=True)  # Actually import now
        sch = 0
        for data in imported_data:
            if sch > 5:
                name = data[1]
                manufacturer = data[2]
                code_of_product = data[3]
                unit = data[4]
                articul = data[5]
                from CMW.services import _save_materials
                _save_materials(name, manufacturer, code_of_product, unit, articul)
            sch += 1
        return redirect('object:materials:plan_materials_view', slug_proj=slug_proj, slug=slug)
    return render(request, 'materials/import_plan_materials.html', {'slug': slug, 'slug_proj': slug_proj, })


def upload_plan_materials(request, slug_proj, slug):
    """Загрузка планируемых материалов из файла .xls"""
    if request.method == 'POST':
        materials_resource = PlanMaterialsResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']
        imported_data = dataset.load(new_persons.read())
        materials_resource.import_data(dataset, dry_run=True)  # Actually import now
        sch = 0
        name_object = Object.objects.get(slug__iexact=slug)
        for data in imported_data:
            if sch > 5:
                name = data[1]
                manufacturer = data[2]
                code_of_product = data[3]
                unit = data[4]
                articul = data[5]
                quantity_plan = data[6]
                if name != None:
                    if quantity_plan != 0:
                        try:
                            Materials.objects.get(articul=articul)
                        except Materials.DoesNotExist:
                            from CMW.services import _save_materials
                            _save_materials(name, manufacturer, code_of_product, unit, articul)
                        try:
                            PlanMaterials.objects.get(material__articul__exact=articul, name_object=name_object)
                        except PlanMaterials.DoesNotExist:
                            material_name = Materials.objects.get(articul=articul)
                            value = PlanMaterials(material=material_name, quantity_plan=quantity_plan,
                                                  quantity_delivered=0,
                                                  name_object=name_object)
                            value.save()
            sch += 1
        return redirect('object:materials:plan_materials_view', slug_proj=slug_proj, slug=slug)
    return render(request, 'materials/import_plan_materials.html', {'slug': slug, 'slug_proj': slug_proj, })


def search_plan_materials(request):
    """Поиск планируемых материалов через строку поиска"""
    form = SearchPlanMaterialsForm(request.POST)
    if form.is_valid():

        q = form.cleaned_data['q']
        slug = form.cleaned_data['slug_o']

        if len(q) == 0:
            plan_materials = PlanMaterials.objects.filter(name_object__slug__exact=slug)

        else:
            if len(q) == 1:
                plan_materials = PlanMaterials.objects.filter(material__name__istartswith=q.upper(),
                                                              name_object__slug__exact=slug)
            else:
                plan_materials = PlanMaterials.objects.filter(material__name__istartswith=q.capitalize(),
                                                              name_object__slug__exact=slug)

                # ---------------------доработать вывод об ошибке
        if not plan_materials:
            error = q + 'не существует в списке'
            context = {'q': q, 'plan_materials': plan_materials, 'error': error}
        else:
            context = {'q': q, 'plan_materials': plan_materials}
        return_str = render_to_string('part_views/search_plan_materials.html', context)
        return HttpResponse(json.dumps(return_str), content_type='application/json')
    else:
        HttpResponseRedirect('object:materials:plan_materials_view')


def export_plan_materials(request, slug_proj, slug):
    """Скачивание планируемых материалов в файл .xls"""
    name_object = Object.objects.get(slug__iexact=slug).Name_Object
    file_name = "Planing_Materials_"
    name_sheet = 'Планируемые материалы ' + name_object

    columns = ['Наименование', 'Планируемое кол-во', 'Поставленное кол-во', 'Ед.измерения', 'Производитель',
               'Код продукта', 'Артикул']
    rows = PlanMaterials.objects.filter(name_object__slug__exact=slug).values_list('material__name',
                                                                                   'quantity_plan',
                                                                                   'quantity_delivered',
                                                                                   'material__unit__name',
                                                                                   'material__manufacturer',
                                                                                   'material__code_of_product',
                                                                                   'material__articul', ).order_by(
        'material__name')
    resp = export_xls(name_object, file_name, name_sheet, columns, rows)
    return resp


def view_plan_materials(request, slug_proj, slug):
    """Отображение списка планируемых материалов"""
    name_object = Object.objects.get(slug__iexact=slug)
    search_form = SearchPlanMaterialsForm()

    plan_material = PlanMaterials.objects.filter(name_object__slug__exact=slug)

    if request.user.is_superuser == True:
        return render(request, "materials/view.html",
                      {'object_list': name_object, 'plan_materials': plan_material, 'search': search_form,
                       'slug': slug, 'slug_proj': slug_proj, 'error_superuser': 'У вас недостаточно прав',
                       })
    if not request.user.has_perm('materials.delete_planmaterials') and not request.user.has_perm(
            'materials.change_planmaterials'):
        return render(request, "materials/view.html",
                      {'object_list': name_object, 'plan_materials': plan_material, 'search': search_form,
                       'slug': slug, 'slug_proj': slug_proj, 'error_perm': 'У вас недостаточно прав',
                       })
    return render(request, 'materials/view.html',
                  {'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object,
                   'plan_materials': plan_material,
                   'search': search_form, })


def create_plan_materials(request, slug_proj, slug):
    """Добавление планируемого материала из БД"""
    form = PlanMaterialsForm()
    name_object = Object.objects.get(slug__iexact=slug)
    if not request.user.has_perm('materials.add_planmaterials'):
        return render(request, "materials/create.html",
                      {'slug': slug, 'slug_proj': slug_proj, 'name_object': name_object,
                       'error_perm': 'У вас недостаточно прав'})
    if request.method == "POST":
        form = PlanMaterialsForm(slug, request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name_object = Object.objects.get(slug__iexact=slug)
            material = data['material']
            plan_material = PlanMaterials.objects.filter(material__name__iexact=material.name,
                                                         name_object__slug__exact=slug)
            if plan_material:
                return render(request, 'materials/create.html',
                              {'form': form, 'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object,
                               'error': 'Данный материал уже есть в списке', })
            # ---------------------------доделать
            else:
                quantity_plan = data['quantity_plan']
                quantity_delivered = data['quantity_delivered']
                add = PlanMaterials(material=material, quantity_plan=quantity_plan,
                                    quantity_delivered=quantity_delivered, name_object_id=name_object.id)
                add.save()
                return redirect('object:materials:plan_materials_view', slug_proj=slug_proj, slug=slug)
    return render(request, 'materials/create.html',
                  {'form': form, 'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object,
                   })


def delete_plan_materials(request, slug_proj, slug, pk):
    """Удаление планируемого материала из БД"""
    material = PlanMaterials.objects.get(pk=pk)
    # -------проверка на доступ
    if not request.user.has_perm('materials.delete_planmaterials'):
        return render(request, "work/delete_plan_work.html",
                      {'slug': slug, 'slug_proj': slug_proj,
                       'error_perm': 'У вас недостаточно прав'})
    if request.method == 'POST':
        material.delete()
        return redirect("object:materials:plan_materials_view", slug_proj=slug_proj, slug=slug)
    name_object = Object.objects.get(slug__iexact=slug)
    return render(request, 'materials/delete.html',
                  {"slug_proj": slug_proj, "slug": slug, "material": material, "pk": pk, 'object_list': name_object})


def update_plan_materials(request, slug_proj, slug, pk):
    """Изменение информации о планируемом материале"""
    # -------проверка на доступ
    if not request.user.has_perm('materials.change_planmaterials'):
        return render(request, "materials/update.html", {'slug': slug, 'slug_proj': slug_proj, 'pk': pk,
                                                         'error_perm': 'У вас недостаточно прав'})
    if request.method == "POST":
        material_form = PlanMaterialsForm(slug, request.POST or None)
        if material_form.is_valid():
            material = PlanMaterials.objects.get(pk=pk, name_object__slug__exact=slug)
            data = material_form.cleaned_data
            material_get = data['material']
            quantity_plan = data['quantity_plan']
            quantity_delivered = data['quantity_delivered']
            if material_get != material.material:
                find_material = PlanMaterials.objects.filter(
                    material__name__iexact=material_get,
                    name_object__slug__iexact=slug)
                if find_material:
                    return render(request, "materials/update.html",
                                  {'slug': slug, 'slug_proj': slug_proj, 'pk': pk, 'form': material_form,
                                   'error': 'Данная работа уже существует в списке'})
                else:
                    if material_get != material.material:
                        material.material = material_get
            if quantity_plan != material.quantity_plan:
                material.quantity_plan = quantity_plan
            if quantity_delivered != material.quantity_delivered:
                material.quantity_delivered = quantity_delivered
            material.save()
            return redirect("object:materials:plan_materials_view", slug_proj=slug_proj, slug=slug)
    material = PlanMaterials.objects.get(pk=pk, name_object__slug__exact=slug)
    material_form = PlanMaterialsForm(slug, instance=material)
    name_object = Object.objects.get(slug__iexact=slug)
    return render(request, "materials/update.html",
                  {'slug': slug, 'slug_proj': slug_proj, 'pk': pk, 'form': material_form, 'object_list': name_object})
