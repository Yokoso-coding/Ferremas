from django.urls import path
from .views import vendedor

urlpatterns = [
    path('inicioVendedor/', vendedor, name='vendedor'),
]