from django.shortcuts import render, redirect

from .forms import CreatePhoto
from .models import Project, CustomUser


def home(request):
    projects = Project.objects.all()
    return render(request, 'project/home.html', {'project_list': projects, })


def upload_photo(request):
    form = CreatePhoto()
    if request.method == 'POST':
        form = CreatePhoto(request.POST, request.FILES)
        if form.is_valid():
            if 'img' in request.FILES:
                user = request.user
                data_user = CustomUser.objects.get(pk=user.pk)
                data_user.delete()
                data_user.img = request.FILES['img']
                data_user.save()
            return redirect('project:home', )
    return render(request, 'part_views/create_photo_form.html', {'form': form})
