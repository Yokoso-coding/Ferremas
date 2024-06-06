
from django.urls import path
from . import views
from .views import contador, generar_pdf

urlpatterns = [
    path('inicioC/', contador, name="bodeguero"),
    path('reportePdf/', generar_pdf, name="reporte_view"),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
]