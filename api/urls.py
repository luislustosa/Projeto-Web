from django.urls import path
from . import views

urlpatterns = [
    path('eventos/', views.EventoList.as_view(), name='eventos-list'),
    path('usuarios/', views.UsuarioList.as_view(), name='usuarios-list'),
]
