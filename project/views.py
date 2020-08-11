import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import CreatePhoto
from .models import Project, CustomUser


def home(request):
    # form = CreatePhoto(request.POST)
    projects = Project.objects.all()
    return render(request, 'project/home.html', {'project_list': projects,})


# def create_photo_form(request):
#     form = CreatePhoto()
#     context = {'form': form}
#     return_str = render_to_string('part_views/create_photo_form.html', context)
#     return HttpResponse(json.dumps(return_str), content_type='application/json')


def upload_photo(request):
    form = CreatePhoto()
    if request.method == 'POST':
        form = CreatePhoto(request.POST, request.FILES)
        if form.is_valid():
            if 'img' in request.FILES:
                user = request.user
                data_user = CustomUser.objects.get(pk=user.pk)
                data_user.img = request.FILES['img']
                data_user.save()
            return redirect('project:home', )
    return render(request, 'part_views/create_photo_form.html', {'form': form})
