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
from .views import home, catalogo_productos, agregar_al_carro, ver_carrito, reducir_cantidad, aumentar_cantidad, eliminar_del_carrito, iniciar_pago, confirmar_pago, registrar_cliente, perfil_cliente, config_cliente, CustomLoginView, CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('catalogo/', catalogo_productos, name='catalogo_productos'),
    path('agregar/<int:producto_id>/', agregar_al_carro, name='agregar_al_carro'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('reducir/<int:id>/', reducir_cantidad, name='reducir_cantidad'),
    path('eliminar/<int:id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('aumentar/<str:key>/', aumentar_cantidad, name='aumentar_cantidad'),
    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
    path('register/', registrar_cliente, name='register'),
    path('profile/', perfil_cliente, name='profile'),
    path('settings/', config_cliente, name='settings'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Definir URL de login
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
