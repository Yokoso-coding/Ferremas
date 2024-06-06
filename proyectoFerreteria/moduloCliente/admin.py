from django.contrib import admin
from .models import Categoria, Producto, Usuario, Pedido, DetallePedido, Promocion, PromocionProducto, PromocionCategoria

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Promocion)
admin.site.register(PromocionProducto)
admin.site.register(PromocionCategoria)