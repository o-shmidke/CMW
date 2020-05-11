from django.urls import path
from .views import home, object_create_view, ObjectUpdateView, ObjectDeleteView

app_name = 'object'
urlpatterns = [
    path('?P<int:pk>', home, name="home"),
    path('objects/add/?P<int:pk>', object_create_view, name="add"),
    path('objects/update/?P<int:pk>', ObjectUpdateView.as_view(), name="update"),
    path('objects/delete/?P<int:pk>', ObjectDeleteView.as_view(), name="delete"),
]
