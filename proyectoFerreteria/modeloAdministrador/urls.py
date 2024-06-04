from django.urls import path
from .views import modeloAdministradorForm

urlpatterns = [
    path('inicio/',crear_usuario, name='administrador')
]