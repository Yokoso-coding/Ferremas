from django.urls import path
from .views import bodeguero

urlpatterns = [
    path('inicio/', bodeguero, name="bodeguero")
]