from typing import KeysView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
]