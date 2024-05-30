from django.db import models

# Create your models here.

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('Cliente', 'Cliente'),
        ('Vendedor', 'Vendedor'),
        ('Bodeguero', 'Bodeguero'),
        ('Contador', 'Contador'),
        ('Administrador', 'Administrador'),
    ]
    
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('completado', 'Completado'),
    ]

    id_pedido = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADOS_PEDIDO, default='pendiente')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pedido {self.id_pedido} - {self.estado}'

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Detalle {self.id_detalle} - Pedido {self.id_pedido}'

class Promocion(models.Model):
    id_promocion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

class PromocionProducto(models.Model):
    id_promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_promocion', 'id_producto')

class PromocionCategoria(models.Model):
    id_promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_promocion', 'id_categoria')

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado')
    ])

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class OrdenesCompra(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    metodo_pago = models.CharField(max_length=255)
    estado_envio = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado')
    ])