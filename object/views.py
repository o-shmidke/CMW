import io
import os

import zipfile
from datetime import datetime

from os import path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView

from project.models import Project, CustomUser
from work.models import PlanWorks
from .forms import ObjectForm, DocumentsForm
from .models import Object, Documents


# from work.views import refresh_nch_spent


def refresh_data_object(slug):
    name_object = Object.objects.get(slug__iexact=slug)
    plan_works = PlanWorks.objects.filter(name_object__slug__iexact=slug)
    NCH_general = 0
    NCH_spent = 0
    for i in plan_works:
        NCH_general += i.NCH_general
        NCH_spent += i.NCH_spent
    NCH_left = NCH_general - NCH_spent
    if NCH_general != 0:
        perform_proc = int((NCH_spent / NCH_general) * 100)
    else:
        perform_proc = 0
    name_object.NCH_General = NCH_general
    name_object.NCH_Spent = NCH_spent
    name_object.NCH_Left = NCH_left
    name_object.Perform_proc = perform_proc
    name_object.save()


# ---------------------------------------обновление процентов выполнения проекта (в БД)
def refresh_peform_proc_project(slug_proj):
    project = Project.objects.filter(slug__iexact=slug_proj)
    objects = Object.objects.filter(ID_Project__slug__iexact=slug_proj)
    perform_proc = [p.Perform_proc for p in objects]
    sum = 0
    sch = 0
    if perform_proc:
        for i in objects:
            sum += perform_proc[sch]
            sch += 1
        if sch != 0:
            perform_proc = int(sum / sch)
        return project.update(Perform_proc=perform_proc)
    return project.update(Perform_proc=0)


# ---------------------------------------обновление процентов выполнения объекта (в БД)
def refresh_peform_proc_objects(slug):
    obj = Object.objects.filter(slug__iexact=slug)
    nch_spent = obj[0].NCH_Spent
    nch_general = obj[0].NCH_General
    if nch_general:
        perform_proc = int((nch_spent / nch_general) * 100)
    else:
        perform_proc = obj[0].Perform_proc
    return obj.update(Perform_proc=perform_proc)


def home(request, slug_proj):
    name_project = Project.objects.get(slug__iexact=slug_proj)
    objects = Object.objects.filter(ID_Project=name_project.pk)

    if not request.user.has_perm('object.change_object') and not request.user.has_perm(
            'object.delete_object') and not request.user.has_perm('object.add_object'):
        return render(request, "object/home.html",
                      {'slug_project': slug_proj, "object_list": objects, "name_project": name_project,
                       'error_perm': 'У вас недостаточно прав', })

    return render(request, 'object/home.html', {"object_list": objects, "name_project": name_project,
                                                "slug_project": slug_proj})


def detail(request, slug, slug_proj):
    name_object = Object.objects.get(slug__iexact=slug)
    if not request.user.has_perm('object.change_object'):
        return render(request, "object/detail.html",
                      {'slug': slug, 'slug_proj': slug_proj, "object_list": name_object,
                       'error_perm': 'У вас недостаточно прав'})
    return render(request, 'object/detail.html', {"object_list": name_object, 'slug': slug, 'slug_proj': slug_proj})


def object_create_view(request, slug_proj):
    object_form = ObjectForm()
    if not request.user.has_perm('object.add_object'):
        return render(request, "object/create.html",
                      {'slug_proj': slug_proj,
                       'error_perm': 'У вас недостаточно прав', })
    if request.method == "POST":
        object_form = ObjectForm(request.POST or None)
        if object_form.is_valid():
            data = object_form.cleaned_data
            id_project = Project.objects.get(slug__iexact=slug_proj).id
            name_object = data['Name_Object']
            adress_object = data['Adress_Object']
            # nch_general = data['NCH_General']
            # -----------------------------------------настроить НЧ потраченные
            nch_spent = 0

            if data['ID_Rukovoditel']:
                rukovoditel = data['ID_Rukovoditel'].pk
            else:
                rukovoditel = ''
            if data['ID_Menedger']:
                manager = data['ID_Menedger'].pk
            else:
                manager = ''
            if data['ID_Ingener']:
                ingener = data['ID_Ingener'].pk
            else:
                ingener = ''
            if data['ID_Montazhnik']:
                montagnik = data['ID_Montazhnik'].pk
            else:
                montagnik = ''

            fio_zakazchika = data['FIO_zakazchika']
            number_phone = str(data['Number_phone'])
            note = data['Note']
            # perform_proc = int((nch_spent / nch_general) * 100)
            perform_proc = 0
            nch_general = 0
            add = Object(Name_Object=name_object, Adress_Object=adress_object, NCH_General=nch_general,
                         NCH_Spent=nch_spent, FIO_zakazchika=fio_zakazchika, Number_phone=number_phone, Note=note,
                         Perform_proc=perform_proc, ID_Project_id=id_project, ID_Rukovoditel_id=rukovoditel,
                         ID_Menedger_id=manager, ID_Ingener_id=ingener, ID_Montazhnik_id=montagnik)
            add.save()
            refresh_peform_proc_project(slug_proj)
            return redirect('object:home', slug_proj=slug_proj)
        else:
            return render(request, "object/create.html",
                          {"form": object_form, 'slug_project': slug_proj, 'error': object_form.errors})

    return render(request, "object/create.html", {"form": object_form, 'slug_project': slug_proj})


class ObjectUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Object
    form_class = ObjectForm
    template_name = 'object/update.html'
    success_message = "Объект успешно изменен"
    login_url = 'login/'

    def get_success_url(self):
        slug_proj = self.kwargs['slug_proj']
        slug = self.kwargs['slug']
        refresh_peform_proc_objects(slug)
        refresh_peform_proc_project(slug_proj)
        return reverse('object:home', kwargs={'slug_proj': slug_proj})

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        slug_proj = self.kwargs['slug_proj']

        name_object = Object.objects.get(slug__iexact=slug)
        obj = Object.objects.get(slug__iexact=slug)
        obj_form = ObjectForm(instance=obj)
        return {'slug_proj': slug_proj, 'slug': slug, 'object_list': name_object,
                'obj_form': obj_form}


def delete(slug):
    objects = Object.objects.get(slug__iexact=slug)
    return objects.delete()


class ObjectDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Object
    template_name = 'object/delete.html'
    success_message = "Объект успешно удален"
    login_url = 'login/'

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        slug_proj = self.kwargs['slug_proj']
        name_object = Object.objects.get(slug__iexact=slug)

        return {'slug_proj': slug_proj, 'slug': slug, 'object_list': name_object}

    def get_success_url(self):
        slug_proj = self.kwargs['slug_proj']
        slug = self.kwargs['slug']
        delete(slug)
        refresh_peform_proc_project(slug_proj)
        return reverse('object:home', kwargs={'slug_proj': slug_proj})


def documents_view(request, slug_proj, slug):
    name_object = Object.objects.get(slug__iexact=slug)
    documents = Documents.objects.filter(name_object__slug__exact=slug)
    if not request.user.has_perm('object.delete_documents') or not request.user.has_perm('object.add_documents'):
        return render(request, 'object/documents.html',
                      {'object_list': name_object, 'documents': documents, 'slug_proj': slug_proj, 'slug': slug,
                       'error_perm': 'У вас недостаточно прав', })
    return render(request, 'object/documents.html',
                  {'object_list': name_object, 'documents': documents, 'slug_proj': slug_proj, 'slug': slug})


def documents_upload(request, slug_proj, slug):
    form = DocumentsForm()
    if request.method == 'POST':
        form = DocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            if 'documents' in request.FILES:
                name_object = Object.objects.get(slug__iexact=slug)
                # name_object.documents = request.FILES['documents']
                files = request.FILES.getlist('documents')
                user = request.user
                user_get = CustomUser.objects.get(id=user.id)
                first_name = '{:.1}.'.format(user_get.first_name)
                patronymic_name = '{:.1}.'.format(user_get.patronymic_name)
                last_name = '{} '.format(user_get.last_name)
                senior = '{} {} {}'.format(last_name, first_name, patronymic_name)
                date = datetime.now()
                for f in files:
                    s = 'documents/' + str(f)
                    name = path.basename(s)
                    add = Documents(documents=f, name_document=name, name_object_id=name_object.pk, date=date,
                                    senior=senior)
                    add.save()

            return redirect('object:documents_view', slug_proj=slug_proj, slug=slug)

    return render(request, 'object/upload_documents_form.html', {'form': form, 'slug_proj': slug_proj, 'slug': slug})


def documents_delete(request, slug_proj, slug, pk):
    doc = Documents.objects.get(pk=pk)
    name_object = Object.objects.get(slug__iexact=slug)
    if request.method == 'POST':
        doc.delete()
        return redirect('object:documents_view', slug_proj=slug_proj, slug=slug)
    return render(request, 'object/delete_documents_form.html',
                  {'slug_proj': slug_proj, 'slug': slug, 'doc': doc, 'object_list': name_object})

# def getfiles(request, slug_proj, slug):
#     # Files (local path) to put in the .zip
#
#     doc = Documents.objects.filter(name_object__slug__exact=slug)
#     filenames = [a.documents.name for a in doc]
#     # filenames = ['Ц15-1_2073-ОВ_v2.pdf', ]
#
#     # Folder name in ZIP archive which contains the above files
#     # E.g [thearchive.zip]/somefiles/file2.txt
#
#     zip_subdir = "media"
#     zip_filename = "%s.zip" % zip_subdir
#
#     # Open StringIO to grab in-memory ZIP contents
#     # s = StringIO.StringIO()
#     s = stringIOModule.StringIO()
#     # The zip compressor
#     zf = zipfile.ZipFile(s, "w")
#
#     for fpath in filenames:
#         # Calculate path for file in zip
#         fdir, fname = os.path.split(fpath)
#         zip_path = os.path.join(zip_subdir, fname)
#
#         # Add file, at correct path
#         zf.write(fpath, zip_path)
#
#     # Must close zip for all contents to be written
#     zf.close()
#
#     # Grab ZIP file from in-memory, make response with correct MIME-type
#     resp = HttpResponse(s.getvalue(), mimetype="application/x-zip-compressed")
#     # ..and correct content-disposition
#     resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
#
#     return resp
