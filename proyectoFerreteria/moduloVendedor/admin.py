from django.contrib import admin
from .models import Categoria, Producto, Usuario, Pedido, DetallePedido, Promocion, PromocionProducto, PromocionCategoria, Carrito, DetalleCarrito, OrdenesCompra

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Promocion)
admin.site.register(PromocionProducto)
admin.site.register(PromocionCategoria)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)
admin.site.register(OrdenesCompra)