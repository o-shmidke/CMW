import kwargs as kwargs
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from project.models import Project
from .forms import ObjectForm
from .models import Object


def home(request, pk):
    name_project = Project.objects.get(pk=pk)
    objects = Object.objects.filter(ID_Project=pk)
    return render(request, 'object/home.html', {"object_list": objects, "name_project": name_project,
                                                "pk_project": pk})


def object_create_view(request, pk):
    object_form = ObjectForm()
    if request.method == "POST":
        object_form = ObjectForm(request.POST or None)
        if object_form.is_valid():
            data = object_form.cleaned_data
            id_project = pk
            name_object = data['Name_Object']
            adress_object = data['Adress_Object']
            nch_general = data['NCH_General']
            nch_spent = 50
            rukovoditel = data['ID_Rukovoditel'].pk
            manager = data['ID_Menedger'].pk
            ingener = data['ID_Ingener'].pk
            montagnik = data['ID_Montazhnik'].pk
            perform_proc = int((nch_spent / nch_general) * 100)
            add = Object(Name_Object=name_object, Adress_Object=adress_object, NCH_General=nch_general,
                         NCH_Spent=nch_spent,
                         Perform_proc=perform_proc, ID_Project_id=id_project, ID_Rukovoditel_id=rukovoditel,
                         ID_Menedger_id=manager, ID_Ingener_id=ingener, ID_Montazhnik_id=montagnik)
            add.save()
            return redirect('object:home', pk=pk)
    return render(request, "object/create.html", {"form": object_form, 'pk_project': pk}, )


class ObjectUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Object
    form_class = ObjectForm
    template_name = 'object/update.html'
    # success_url = reverse_lazy('object:home')
    success_message = "Объект успешно изменен"
    login_url = 'login/'

    def get_success_url(self):
        # ---------------------------------------нужно настроить перенаправление на страницу объектов
        obj = self.kwargs['pk']
        return reverse('object:home', kwargs={'pk': obj})


class ObjectDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Object
    template_name = 'object/delete.html'
    success_url = reverse_lazy('project:home')
    login_url = 'login/'

    # def get(self, request, *args, **kwargs):
    #     messages.success(request, 'Поезд удален')
    #     return self.post(request, *args, *kwargs)
