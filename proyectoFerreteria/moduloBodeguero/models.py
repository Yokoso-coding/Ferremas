from django.db import models
from moduloCliente.models import Producto, DetallePedido
#from moduloCliente.models import Pedido

class DetalleBodega(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'Detalle de {self.producto.nombre} - Cantidad {self.cantidad}'