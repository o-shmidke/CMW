import json

import xlwt
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DeleteView

from CMW.utils import export_xls
from project.models import CustomUser
from utils.uploading import UploadingPlanWorks
from .forms import PlanWorksForm, CompleteWorksForm, SearchWorksForm, CheckCompleteWorksForm
from .models import *


def color_proc(perform_proc):
    color = ()
    if perform_proc <= 100:
        max = 100

        fromR = 255
        fromG = 0
        fromB = 0

        toR = 0
        toG = 255
        toB = 0
        a = ()
        deltaR = round((toR - fromR) / max)
        deltaG = round((toG - fromG) / max)
        deltaB = round((toB - fromB) / max)
        # for i in t:
        R = fromR + perform_proc * deltaR
        G = fromG + perform_proc * deltaG
        B = fromB + perform_proc * deltaB
        a = R, G, B
        color += a
    else:
        R = 0
        G = 107
        B = 169
        a = R, G, B
        color += a
    return a


def refresh_nch_general_object(name_object):
    NCH_general_object = [p.NCH_general for p in PlanWorks.objects.filter(name_object=name_object.id)]
    if NCH_general_object:
        NCH_general_sum = 0
        for i in NCH_general_object:
            NCH_general_sum += i
        name_object.NCH_General = NCH_general_sum
    else:
        name_object.NCH_General = 0
    name_object.save()
    return 0


def search_complete_works(request):
    form = SearchWorksForm(request.POST)
    if form.is_valid():
        q = form.cleaned_data['q']
        slug = form.cleaned_data['slug_o']
        slug_proj = form.cleaned_data['slug_p']

        if len(q) == 0:
            complete_works = CompleteWorks.objects.filter(name_object__slug__iexact=slug)
        else:
            if len(q) == 1:
                complete_works = CompleteWorks.objects.filter(type_works__name__istartswith=q.upper(),
                                                              name_object__slug__iexact=slug)

            else:
                complete_works = CompleteWorks.objects.filter(type_works__name__icontains=q.capitalize(),
                                                              name_object__slug__iexact=slug)

        context = {'q': q, 'complete_work': complete_works, 'slug': slug, 'slug_proj': slug_proj}
        return_str = render_to_string('part_views/search_complete_work.html', context)
        return HttpResponse(json.dumps(return_str), content_type='application/json')
    else:
        HttpResponseRedirect('work:plan_work')


def search_plan_works(request):
    form = SearchWorksForm(request.POST)
    if form.is_valid():
        q = form.cleaned_data['q']
        slug = form.cleaned_data['slug_o']
        slug_proj = form.cleaned_data['slug_p']
        group = Groups.objects.all()
        plan_work = {}

        if len(q) == 0:
            for y in group:
                plan_work[y.name] = PlanWorks.objects.filter(type_works__group__name__iexact=y.name,
                                                             name_object__slug__exact=slug)
        else:
            if len(q) == 1:
                for y in group:
                    plan_work[y.name] = PlanWorks.objects.filter(type_works__name__istartswith=q.upper(),
                                                                 type_works__group__name__iexact=y.name,
                                                                 name_object__slug__exact=slug)
            else:
                for y in group:
                    plan_work[y.name] = PlanWorks.objects.filter(type_works__name__icontains=q.capitalize(),
                                                                 type_works__group__name__iexact=y.name,
                                                                 name_object__slug__exact=slug)
        if not request.user.has_perm('work.delete_planworks') and not request.user.has_perm('work.change_planworks'):
            context = {'q': q, 'plan_work': plan_work, 'slug': slug, 'slug_proj': slug_proj,
                       'error_perm': 'У вас недостаточно прав'}
        else:
            context = {'q': q, 'plan_work': plan_work, 'slug': slug, 'slug_proj': slug_proj}
        return_str = render_to_string('part_views/search_plan_works.html', context)
        return HttpResponse(json.dumps(return_str), content_type='application/json')
    else:
        HttpResponseRedirect('work:plan_work')


def export_plan_work(request, slug_proj, slug):
    name_object = Object.objects.get(slug__iexact=slug).Name_Object
    file_name = 'Planing Work '
    name_sheet = "Планируемые работы"
    columns = ['Вид работ', 'Планируемое колличество', 'Выполненное колличество', 'Ед. измерения',
               'Н/Ч на ед.врем', 'Н/Ч итого', 'Н/Ч затрачено', 'Н/Ч осталось', 'Выполнено', 'Примечание']
    rows = PlanWorks.objects.filter(name_object__slug__exact=slug).values_list('type_works__name', 'quantity_plan',
                                                                               'quantity_complete',
                                                                               'type_works__unit__name',
                                                                               'type_works__NCH_unit_of_time',
                                                                               'NCH_general',
                                                                               'NCH_spent', 'NCH_left', 'perform_proc',
                                                                               'comment',
                                                                               ).order_by('type_works__name')
    resp = export_xls(name_object, file_name, name_sheet, columns, rows)
    return resp


def export_complete_work(request, slug_proj, slug):
    name_object = Object.objects.get(slug__iexact=slug).Name_Object
    file_name = 'JR '
    name_sheet = "ЖР"
    columns = ['Дата', 'Вид работ', 'Колличество выполнено', 'Ед. измерения', 'Примечание', 'Ответственный']
    rows = CompleteWorks.objects.filter(name_object__slug__exact=slug).values_list('date',
                                                                                   'type_works__name',
                                                                                   'quantity_complete',
                                                                                   'type_works__unit__name', 'comment',
                                                                                   'senior').order_by('date')
    resp = export_xls(name_object, file_name, name_sheet, columns, rows)
    return resp


# -----------------не работает
def download_plan_works(request, slug_proj, slug):
    if request.POST:
        print(request.POST)
        print(request.FILES)
        file = request.FILES['file']
        uploading_file = UploadingPlanWorks({'file': file})
        if uploading_file:
            messages.success(request, 'Успешная загрузка файла')
        else:
            messages.error(request, 'Ошибка при загрузке')
    return render(request, 'work/download_plan_works.html', {'slug_proj': slug_proj, 'slug': slug})


def plan_work_view(request, slug, slug_proj):
    name_object = Object.objects.get(slug__iexact=slug)
    plan_work = PlanWorks.objects.filter(name_object=name_object.id)
    plan_work_nch_general = [p.NCH_general for p in plan_work]
    sum = 0
    sch = 0
    if plan_work_nch_general:
        for i in plan_work_nch_general:
            a = plan_work_nch_general[sch]
            sum += a
            sch += 1

    perform_proc = list()
    sum_proc = 0
    complete_work = [p.type_works for p in PlanWorks.objects.filter(name_object=name_object)]
    form_search = SearchWorksForm()
    if complete_work:

        for y in complete_work:
            complete_works = [p.perform_proc for p in
                              CompleteWorks.objects.filter(type_works=y.pk, name_object=name_object)]
            max = 0
            for i in complete_works:
                if i > max:
                    max = i
            sum_proc += max
            perform_proc.append(sum_proc)

            group = Groups.objects.all()
            plan_work = {}
            for y in group:
                plan_work[y.name] = PlanWorks.objects.filter(type_works__group_id=y.id, name_object__slug__exact=slug)

            # --------------------------------------Проверка на доступ
        if not request.user.has_perm('work.delete_planworks') and not request.user.has_perm('work.change_planworks'):
            return render(request, "work/plan_work.html",
                          {'object_list': name_object, 'plan_work': plan_work, 'slug_proj': slug_proj, 'slug': slug,
                           'nch_sum': sum, 'proc_sum': sum_proc, 'error_perm': 'У вас недостаточно прав',
                           'form': form_search})

        return render(request, 'work/plan_work.html',
                      {'object_list': name_object, 'plan_work': plan_work, 'slug_proj': slug_proj, 'slug': slug,
                       'nch_sum': sum, 'proc_sum': sum_proc, 'form': form_search})

    return render(request, 'work/plan_work.html',
                  {'object_list': name_object, 'plan_work': plan_work, 'slug_proj': slug_proj, 'slug': slug,
                   'nch_sum': sum, 'proc_sum': sum_proc, 'form': form_search})


def plan_work_create(request, slug_proj, slug):
    work_form = PlanWorksForm(slug)
    name_object = Object.objects.get(slug__iexact=slug)
    # ---------------проверка прав
    if not request.user.has_perm('work.add_planworks'):
        return render(request, "work/create_plan_work.html",
                      {'slug': slug, 'slug_proj': slug_proj, 'name_object': name_object,
                       'error_perm': 'У вас недостаточно прав'})

    if request.method == "POST":
        work_form = PlanWorksForm(slug, request.POST or None)
        if work_form.is_valid():
            data = work_form.cleaned_data
            name_object = Object.objects.get(slug__iexact=slug)
            type_works = data['type_works']
            find_works = PlanWorks.objects.filter(type_works__name__iexact=type_works.name,
                                                  name_object__slug__exact=slug)
            if find_works:
                return render(request, "work/create_plan_work.html",
                              {"form": work_form, 'slug': slug, 'slug_proj': slug_proj,
                               'name_object': name_object, 'error': 'Данная работа уже существует в списке'})
            quantity_plan = data['quantity_plan']
            NCH_unit_of_time = TypeOfWork.objects.get(name=type_works.name).NCH_unit_of_time
            NCH_general = quantity_plan * NCH_unit_of_time
            comment = data['comment']

            NCH_left = NCH_general

            color = (255, 0, 0)
            add = PlanWorks(name_object=name_object, type_works=type_works, quantity_plan=quantity_plan,
                            NCH_general=NCH_general, NCH_left=NCH_left, comment=comment, color=color)
            add.save()

            from object.views import refresh_data_object
            refresh_data_object(slug)
            from object.views import refresh_peform_proc_project
            refresh_peform_proc_project(slug_proj)
            return redirect('work:plan_work', slug_proj=slug_proj, slug=slug)
    name_object = Object.objects.get(slug__iexact=slug)
    return render(request, 'work/create_plan_work.html',
                  {'form': work_form, 'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object})


def delete_plan_work(request, slug, slug_proj, pk):
    name_object = Object.objects.get(slug__iexact=slug)
    plan_work = PlanWorks.objects.get(pk=pk)
    if not request.user.has_perm('work.delete_planworks'):
        return render(request, "work/delete_plan_work.html",
                      {'slug': slug, 'slug_proj': slug_proj,
                       'error_perm': 'У вас недостаточно прав', 'object_list': name_object})

    if request.method == "POST":
        plan_work.delete()

        from object.views import refresh_data_object
        refresh_data_object(slug)
        from object.views import refresh_peform_proc_project
        refresh_peform_proc_project(slug_proj)
        return redirect("work:plan_work", slug_proj=slug_proj, slug=slug)

    return render(request, 'work/delete_plan_work.html',
                  {'slug_proj': slug_proj, 'slug': slug, 'pk': pk, 'work': plan_work, 'object_list': name_object})


def plan_work_update(request, slug_proj, slug, pk):
    work = PlanWorks.objects.get(pk=pk)
    work_form = PlanWorksForm(slug, instance=work)
    # --------------------------------------Проверка на доступ
    if not request.user.has_perm('work.change_planworks'):
        return render(request, "work/update_plan_work.html",
                      {'slug_proj': slug_proj, 'slug': slug, 'error_perm': 'У вас недостаточно прав'})
    if request.method == "POST":
        work_form = PlanWorksForm(slug, request.POST or None)
        if work_form.is_valid():
            data = work_form.cleaned_data

            type_works = data['type_works']
            quantity_plan = data['quantity_plan']
            NCH_unit_of_time = TypeOfWork.objects.get(name=type_works.name).NCH_unit_of_time
            comment = data['comment']
            NCH_general = quantity_plan * NCH_unit_of_time
            if quantity_plan != work.quantity_plan:
                if comment:
                    comment += '. План.кол-во изменилось с ' + str(work.quantity_plan) + ' на ' + str(quantity_plan)
                else:
                    comment += 'План.кол-во изменилось с ' + str(work.quantity_plan) + ' на ' + str(quantity_plan)

            if quantity_plan > work.quantity_plan:
                raznost = quantity_plan - work.quantity_plan
                quantity_plan = work.quantity_plan + raznost
                NCH_general = quantity_plan * NCH_unit_of_time

            if quantity_plan < work.quantity_plan:
                raznost = work.quantity_plan - quantity_plan
                quantity_plan = work.quantity_plan - raznost
                NCH_general = quantity_plan * NCH_unit_of_time

            NCH_left = NCH_general - work.NCH_spent
            perform_proc = int((work.NCH_spent / NCH_general) * 100)
            color = color_proc(perform_proc)
            work.quantity_plan = quantity_plan
            work.NCH_general = NCH_general
            work.type_works = type_works
            work.comment = comment
            work.NCH_left = NCH_left
            work.color = color
            work.perform_proc = perform_proc
            work.save()

            from object.views import refresh_data_object
            refresh_data_object(slug)
            from object.views import refresh_peform_proc_project
            refresh_peform_proc_project(slug_proj)
            return redirect('work:plan_work', slug_proj=slug_proj, slug=slug)
    name_object = Object.objects.get(slug__iexact=slug)
    return render(request, 'work/update_plan_work.html',
                  {'form': work_form, 'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object, 'pk': pk})


# ------------------------------------------------------Выполненные работы--------------------------------------------


def complete_work_view(request, slug, slug_proj):
    name_object = Object.objects.get(slug__iexact=slug)
    complete_work = CompleteWorks.objects.filter(name_object=name_object.id)
    x = 2
    plan_work_NCH_general = PlanWorks.objects.filter(name_object=name_object.id)
    return render(request, 'work/complete_work.html',
                  {'object_list': name_object, 'complete_work': complete_work, 'plan_work': plan_work_NCH_general,
                   'slug_proj': slug_proj, 'slug': slug,
                   'nch_left_sum': name_object.NCH_Left, 'nch_spent_sum': name_object.NCH_Spent,
                   'perform_proc_sum': name_object.Perform_proc, 'x': x})


def complete_work_create(request, slug_proj, slug):
    work_form = CompleteWorksForm(slug)
    check_form = CheckCompleteWorksForm(slug)
    name_object = Object.objects.get(slug__iexact=slug)
    if request.method == "POST":
        work_form = CompleteWorksForm(slug, request.POST or None)
        check_form = CheckCompleteWorksForm(slug, request.POST or None)
        if work_form.is_valid():
            data = work_form.cleaned_data
            type_works = work_form.cleaned_data['type_works']
            date = data['date']
            find_works = CompleteWorks.objects.filter(date=date, type_works__name__iexact=type_works.name,
                                                      name_object__slug__exact=slug)
            if not find_works:
                name_object = Object.objects.get(slug__iexact=slug)
                comment = data['comment']
                type_work = TypeOfWork.objects.get(name=type_works.name)
                quantity_complete = data['quantity_complete']
                NCH_unit_of_time = TypeOfWork.objects.get(name=type_works.name).NCH_unit_of_time
                general_spent = [p.NCH_spent for p in
                                 CompleteWorks.objects.filter(name_object=name_object)]
                # ------------------------выдает ошибку при нахождении одинаковых строк
                NCH_general = PlanWorks.objects.get(type_works=type_work, name_object__slug__iexact=slug).NCH_general
                # --------------------------считает затраченные часы для выполненной работы
                complete_works = [p.NCH_spent for p in
                                  CompleteWorks.objects.filter(type_works=type_work, name_object__slug__iexact=slug)]
                max = 0
                sum = 0
                if complete_works:
                    for i in complete_works:
                        if i > max:
                            max = i
                    sum += max
                    NCH_spent = (quantity_complete * NCH_unit_of_time) + sum

                else:
                    NCH_spent = quantity_complete * NCH_unit_of_time

                perform_proc = int((NCH_spent / NCH_general) * 100)
                NCH_left = NCH_general - NCH_spent

                user = request.user
                user_get = CustomUser.objects.get(id=user.id)
                first_name = '{:.1}.'.format(user_get.first_name)
                patronymic_name = '{:.1}.'.format(user_get.patronymic_name)
                last_name = '{} '.format(user_get.last_name)
                senior = '{} {} {}'.format(last_name, first_name, patronymic_name)
                plan_work = PlanWorks.objects.get(type_works=type_work.pk, name_object=name_object)
                color = color_proc(perform_proc)

                add = CompleteWorks(name_object=name_object, type_works=type_work, quantity_complete=quantity_complete,
                                    NCH_spent=NCH_spent, comment=comment, NCH_left=NCH_left, senior=senior,
                                    perform_proc=perform_proc, date=date, plan=plan_work, color=color)
                add.save()
                plan_work.quantity_complete += quantity_complete
                plan_work.NCH_spent = NCH_spent
                plan_work.NCH_left = NCH_left
                plan_work.perform_proc = perform_proc
                plan_work.color = color
                plan_work.save()

                from object.views import refresh_data_object
                refresh_data_object(slug)

                from object.views import refresh_peform_proc_project
                refresh_peform_proc_project(slug_proj)
                return redirect('work:complete_work', slug_proj=slug_proj, slug=slug)
            else:
                return render(request, "work/create_complete_work.html",
                              {"form": work_form, 'slug': slug, 'slug_proj': slug_proj, 'name_object': name_object,
                               'error': 'Данная работа уже существует в этот день', 'check_form': check_form,'object_list':name_object})

    return render(request, 'work/create_complete_work.html',
                  {'form': work_form, 'slug': slug, 'slug_proj': slug_proj, 'name_object': name_object,
                   'check_form': check_form, 'object_list':name_object})


def delete_complete_work(pk, slug):
    comp_work = CompleteWorks.objects.get(pk=pk)
    plan_work = PlanWorks.objects.get(pk=comp_work.plan.pk)

    object = Object.objects.get(slug__iexact=slug)
    NCH_spent_work = (comp_work.quantity_complete * plan_work.type_works.NCH_unit_of_time)
    perf_proc = plan_work.perform_proc - int((NCH_spent_work / plan_work.NCH_general) * 100)
    nch_spent = comp_work.NCH_spent
    nch_left = comp_work.NCH_left
    perform_proc = comp_work.perform_proc
    quantity_complete = comp_work.quantity_complete
    comp_work.delete()
    a = CompleteWorks.objects.filter(type_works__name__iexact=comp_work.type_works.name, name_object__slug__exact=slug)

    if not a:
        plan_work.NCH_spent = 0
        plan_work.NCH_left = plan_work.NCH_general
        plan_work.quantity_complete = 0
    else:
        if plan_work.perform_proc >= 100:
            plan_work.NCH_left += plan_work.NCH_general - quantity_complete * plan_work.type_works.NCH_unit_of_time

            plan_work.NCH_spent -= quantity_complete * plan_work.type_works.NCH_unit_of_time
            plan_work.quantity_complete -= quantity_complete
        else:
            plan_work.NCH_left += nch_left
            plan_work.NCH_spent -= nch_spent
            plan_work.quantity_complete -= quantity_complete
    plan_work.perform_proc = perf_proc
    plan_work.color = color_proc(perf_proc)

    if plan_work.perform_proc < 0:
        plan_work.perform_proc = 0
    plan_work.save()
    return 0


class CompleteWorksDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = CompleteWorks
    template_name = 'work/delete_complete_work.html'
    success_message = "Работа(план) успешно удалена"
    login_url = 'login/'

    def get_success_url(self):
        slug = self.kwargs['slug']
        slug_proj = self.kwargs['slug_proj']
        pk = self.kwargs['pk']
        delete_complete_work(pk, slug)
        from object.views import refresh_data_object
        refresh_data_object(slug)
        from object.views import refresh_peform_proc_project
        refresh_peform_proc_project(slug_proj)
        return reverse('work:complete_work', kwargs={'slug': slug, 'slug_proj': slug_proj})

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        slug_proj = self.kwargs['slug_proj']
        pk = self.kwargs['pk']
        name_object = Object.objects.get(slug__iexact=slug)
        work = CompleteWorks.objects.get(pk=pk)
        return {'slug_proj': slug_proj, 'slug': slug, 'pk': pk, 'work': work, 'object_list': name_object}


def complete_work_update(request, slug_proj, slug, pk):
    work = CompleteWorks.objects.get(pk=pk)
    work_form = CompleteWorksForm(slug, instance=work)
    if request.method == "POST":
        work_form = CompleteWorksForm(slug, request.POST or None)
        if work_form.is_valid():
            data = work_form.cleaned_data
            name_object = Object.objects.get(slug__iexact=slug)

            plan_work = PlanWorks.objects.get(pk=work.plan.pk)
            type_works = data['type_works']
            quantity_complete = data['quantity_complete']
            NCH_unit_of_time = TypeOfWork.objects.get(name=type_works.name).NCH_unit_of_time
            comment = data['comment']
            date = data['date']
            NCH_general = work.plan.NCH_general
            NCH_spent = quantity_complete * NCH_unit_of_time
            NCH_left = NCH_general - NCH_spent
            if date != work.date or type_works != work.type_works:
                find_works = CompleteWorks.objects.filter(date=date, type_works__name__iexact=type_works.name,
                                                          name_object__slug__exact=slug)
                if find_works:
                    return render(request, "work/update_complete_work.html",
                                  {"form": work_form, 'slug': slug, 'slug_proj': slug_proj, 'pk': pk,
                                   'name_object': name_object, 'error': 'Данная работа уже существует в этот день'})

            if quantity_complete != work.quantity_complete:
                complete_works = [p.NCH_spent for p in
                                  CompleteWorks.objects.filter(type_works=type_works, name_object=name_object)]
                max = 0
                sum = 0
                if len(complete_works) > 1:
                    for i in complete_works:
                        if i > max:
                            max = i
                    sum += max

                    raznost = (quantity_complete - work.quantity_complete) * NCH_unit_of_time
                    NCH_spent = raznost + sum
                else:
                    NCH_spent = quantity_complete * NCH_unit_of_time

                perform_proc = int((NCH_spent / NCH_general) * 100)
                color = color_proc(perform_proc)
                work.quantity_complete = quantity_complete
                work.NCH_left = NCH_left
                work.NCH_spent = NCH_spent
                work.color = color
                work.perform_proc = perform_proc

                plan_work.quantity_complete = quantity_complete
                plan_work.NCH_left = NCH_left
                plan_work.NCH_spent = NCH_spent
                plan_work.color = color
                plan_work.perform_proc = perform_proc
            if date != work.date:
                work.date = date
            if comment != work.comment:
                work.comment = comment

            work.type_works = type_works

            work.save()
            plan_work.save()

            from object.views import refresh_data_object
            refresh_data_object(slug)

            from object.views import refresh_peform_proc_project
            refresh_peform_proc_project(slug_proj)
            return redirect('work:complete_work', slug_proj=slug_proj, slug=slug)

    name_object = Object.objects.get(slug__iexact=slug)
    return render(request, 'work/update_complete_work.html',
                  {'form': work_form, 'slug': slug, 'slug_proj': slug_proj, 'object_list': name_object, 'pk': pk})


def check_complete_work(request, slug_proj, slug):
    # form = CheckCompleteWorksForm()

    if request.method == "POST":
        form = CheckCompleteWorksForm(slug, request.POST or None)
        # type_works = form.clean_type_works()
        if form.is_valid():
            type_works = form.cleaned_data['type_works']
            slug = form.cleaned_data['slug_o']
            plan_work = PlanWorks.objects.get(name_object__slug__exact=slug, type_works__pk=type_works.pk)
            # type_works = form.cleaned_data['type_works']
            # slug = form.cleaned_data['slug_o']
            # slug_proj = form.cleaned_data['slug_p']

            # if len(q) == 0:
            #     complete_works = CompleteWorks.objects.filter(name_object__slug__iexact=slug)
            # else:
            #     if len(q) == 1:
            #         complete_works = CompleteWorks.objects.filter(type_works__name__istartswith=q.upper(),
            #                                                       name_object__slug__iexact=slug)
            #
            #     else:
            #         complete_works = CompleteWorks.objects.filter(type_works__name__icontains=q.capitalize(),
            #                                                       name_object__slug__iexact=slug)

            context = {'quantity_plan': plan_work.quantity_plan, 'quantity_complete': plan_work.quantity_complete,
                       'type_works': type_works}
            return_str = render_to_string('part_views/check_complete_works.html', context)
            return HttpResponse(json.dumps(return_str), content_type='application/json')
        else:
            HttpResponseRedirect('work:plan_work')
    else:
        HttpResponseRedirect('work:plan_work')
