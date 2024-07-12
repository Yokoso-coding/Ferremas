from django.urls import path
from .views import vendedor, busquedaVendedor, catalogoVendedor, pedidoVendedor, agregar_al_carrito_vendedor, ver_carrito_vendedor, reducir_cantidad_vendedor, eliminar_del_carrito_vendedor, iniciar_pago_vendedor, confirmar_pago_vendedor
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('inicioVendedor/', vendedor, name='vendedor'),
    path('busquedaVendedor/', busquedaVendedor, name='busquedaVendedor'),
    path('catalogoVendedor/', catalogoVendedor, name='catalogoVendedor'),
    path('pedidoVendedor/', pedidoVendedor, name='pedidoVendedor'),
    path('agregar/<int:producto_id>/', agregar_al_carrito_vendedor, name='agregar_al_carrito_vendedor'),
    path('carritoVendedor/', ver_carrito_vendedor, name='ver_carrito_vendedor'),
    path('reducir/<int:producto_id>/', reducir_cantidad_vendedor, name='reducir_cantidad_vendedor'),
    path('eliminar/<int:producto_id>/', eliminar_del_carrito_vendedor, name='eliminar_del_carrito_vendedor'),
    path('iniciar_pago/', iniciar_pago_vendedor, name='iniciar_pago_vendedor'),
    path('confirmar_pago/', confirmar_pago_vendedor, name='confirmar_pago_vendedor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)