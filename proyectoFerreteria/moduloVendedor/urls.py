from django.urls import path
from .views import home_vendedor, perfil_cliente_vendedor, config_cliente_vendedor, catalogo_productos_vendedor, agregar_al_carro_vendedor, aumentar_cantidad_vendedor, reducir_cantidad_vendedor, eliminar_del_carrito_vendedor, ver_carrito_vendedor, iniciar_pago_vendedor, confirmar_pago_vendedor, CustomLoginView, CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index_vendedor.html'), name='home_vendedor'),
    path('catalogo_vendedor/', catalogo_productos_vendedor, name='catalogo_productos_vendedor'),
    path('agregar_vendedor/<int:producto_id>/', agregar_al_carro_vendedor, name='agregar_al_carro_vendedor'),
    path('carrito_vendedor/', ver_carrito_vendedor, name='ver_carrito_vendedor'),
    path('reducir_vendedor/<int:id>/', reducir_cantidad_vendedor, name='reducir_cantidad_vendedor'),
    path('eliminar_vendedor/<int:id>/', eliminar_del_carrito_vendedor, name='eliminar_del_carrito_vendedor'),
    path('aumentar_vendedor/<str:key>/', aumentar_cantidad_vendedor, name='aumentar_cantidad_vendedor'),
    path('iniciar_pago_vendedor/', iniciar_pago_vendedor, name='iniciar_pago_vendedor'),
    path('confirmar_pago_vendedor/', confirmar_pago_vendedor, name='confirmar_pago_vendedor'),
    path('perfil_vendedor/', perfil_cliente_vendedor, name='perfil_cliente_vendedor'),
    path('config_vendedor/', config_cliente_vendedor, name='config_cliente_vendedor'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Definir URL de login
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)