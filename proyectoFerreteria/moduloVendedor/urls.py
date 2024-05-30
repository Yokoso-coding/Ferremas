from django.urls import path
from .views import vendedor, agregar_al_carrito, ver_carrito, reducir_cantidad, eliminar_del_carrito, iniciar_pago, confirmar_pago
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('inicioVendedor/', vendedor, name='vendedor'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('reducir/<int:producto_id>/', reducir_cantidad, name='reducir_cantidad'),
    path('eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)