from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import bodeguero

urlpatterns = [
    path('inicio/', bodeguero, name="bodeguero"),
    path('pedido/', views.pedido_bodeguero, name="bodeguerop"),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/actualizar/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)