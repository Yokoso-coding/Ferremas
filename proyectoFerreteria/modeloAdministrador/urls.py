from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.crear_usuario, name='administrador'),
    path('redireccion/', views.redireccion, name='redireccion'),
]