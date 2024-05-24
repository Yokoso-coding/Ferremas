"""
URL configuration for proyectoFerreteria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import home, catalogo_productos, agregar_al_carrito, ver_carrito, reducir_cantidad, eliminar_del_carrito, iniciar_pago, confirmar_pago
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('catalogo/', catalogo_productos, name='catalogo_productos'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('reducir/<int:producto_id>/', reducir_cantidad, name='reducir_cantidad'),
    path('eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
