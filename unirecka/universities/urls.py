from django.urls import path
from . import views

urlpatterns = [
    path('', views.university_list, name='university_list'),
]