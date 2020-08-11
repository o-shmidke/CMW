import json


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.template.loader import render_to_string

from CMW.utils import export_xls

from materials.forms import PlanMaterialsForm, SearchPlanMaterialsForm
from .models import *



def search_plan_materials(request):
    form = SearchPlanMaterialsForm(request.POST)
    if form.is_valid():
        group = Groups.objects.all()
        plan_materials = {}
        q = form.cleaned_data['q']
        slug = form.cleaned_data['slug_o']

        if len(q) == 0:
            # plan_materials = PlanMaterials.objects.filter(name_object__slug__exact=slug)
            for y in group:
                plan_materials[y.name] = PlanMaterials.objects.filter(group=y.id, name_object__slug__exact=slug)

        else:
            if len(q) == 1:
                # plan_materials = PlanMaterials.objects.filter(material__name__istartswith=q.upper(),
                #                                               name_object__slug__exact=slug)

                for y in group:
                    plan_materials[y.name] = PlanMaterials.objects.filter(group=y.id,
                                                                          material__name__istartswith=q.upper(),
                                                                          name_object__slug__exact=slug)
            else:
                # plan_materials = PlanMaterials.objects.filter(material__name__icontains=q.capitalize(),
                #                                               name_object__slug__exact=slug)

                for y in group:
                    plan_materials[y.name] = PlanMaterials.objects.filter(group=y.id,
                                                                          material__name__istartswith=q.capitalize(),
                                                                          name_object__slug__exact=slug)

                    # ---------------------доработать вывод об ошибке
        if not plan_materials:
            error = 'error'

        context = {'q': q, 'plan_materials': plan_materials}
        return_str = render_to_string('part_views/search_plan_materials.html', context)
        return HttpResponse(json.dumps(return_str), content_type='application/json')
    else:
        HttpResponseRedirect('object:materials:plan_materials_view')


def export_plan_materials(request, slug_proj, slug):
    name_object = Object.objects.get(slug__iexact=slug).Name_Object
    file_name = "Planing Materials "
    name_sheet = 'Планируемые материалы ' + name_object
    columns = ['Наименование', 'Планируемое кол-во', 'Поставленное кол-во', 'Ед.измерения', ]
    rows = PlanMaterials.objects.filter(name_object__slug__exact=slug).values_list('material__name',
                                                                                   'quantity_plan',
                                                                                   'quantity_delivered',
                                                                                   'material__unit__name', ).order_by(
        'material__name')
    resp = export_xls(name_object, file_name, name_sheet, columns, rows)
    return resp


def view_plan_materials(request, slug_proj, slug):
    name_object = Object.objects.get(slug__iexact=slug)
    search_form = SearchPlanMaterialsForm()

    plan_material = PlanMaterials.objects.filter(name_object__slug__exact=slug)
    group = Groups.objects.all()
    plan_materials = {}

    for y in group:
        plan_materials[y.name] = PlanMaterials.objects.filter(group=y.id, name_object__slug__exact=slug)
    if not request.user.has_perm('materials.delete_planmaterials') and not request.user.has_perm(
            'materials.change_planmaterials'):
        return render(request, "materials/view.html",
                      {'object_list': name_object, 'plan_materials': plan_materials, 'search': search_form,
                       'slug': slug, 'slug_proj': slug_proj, 'error_perm': 'У вас недостаточно прав',
                       })
    return render(request, 'materials/view.html',
                  {'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object,
                   'plan_materials': plan_materials,
                   'search': search_form, })


def create_plan_materials(request, slug_proj, slug):
    form = PlanMaterialsForm()
    name_object = Object.objects.get(slug__iexact=slug)
    if not request.user.has_perm('materials.add_planmaterials'):
        return render(request, "materials/create.html",
                      {'slug': slug, 'slug_proj': slug_proj, 'name_object': name_object,
                       'error_perm': 'У вас недостаточно прав'})
    if request.method == "POST":
        form = PlanMaterialsForm(slug, request.POST or None)
        a = form.is_valid()
        if form.is_valid():
            data = form.cleaned_data
            name_object = Object.objects.get(slug__iexact=slug)
            material = data['material']
            group = data['group']
            plan_material = PlanMaterials.objects.filter(material__name__iexact=material.name,
                                                         material__planmaterials__group__exact=group.id,
                                                         name_object__slug__exact=slug)
            if plan_material:
                return render(request, 'materials/create.html',
                              {'form': form, 'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object,
                               'error': 'Данный материал уже есть в списке', })
            # ---------------------------доделать
            else:
                quantity_plan = data['quantity_plan']
                quantity_delivered = data['quantity_delivered']
                add = PlanMaterials(material=material, quantity_plan=quantity_plan, group_id=group.id,
                                    quantity_delivered=quantity_delivered, name_object_id=name_object.id)
                add.save()
                return redirect('object:materials:plan_materials_view', slug_proj=slug_proj, slug=slug)
    return render(request, 'materials/create.html',
                  {'form': form, 'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object,
                   })


def delete_plan_materials(request, slug_proj, slug, pk):
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
            group = data['group']

            if material_get != material.material or group != material.group:
                find_material = PlanMaterials.objects.filter(group__name__iexact=group,
                                                             material__name__iexact=material_get,
                                                             name_object__slug__iexact=slug)
                if find_material:
                    return render(request, "materials/update.html",
                                  {'slug': slug, 'slug_proj': slug_proj, 'pk': pk, 'form': material_form,
                                   'error': 'Данная работа уже существует в списке'})
                else:
                    if material_get != material.material:
                        material.material = material_get
                    if group != material.group:
                        material.group = group

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
