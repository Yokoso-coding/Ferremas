
from django.urls import path
from . import views
from .views import contador

urlpatterns = [
    path('inicioC/', contador, name="bodeguero"),
]