from django.db import models

OPCIONES_USUARIO = [
    ('cliente', 'Cliente'),
    ('vendedor', 'Vendedor'),
    ('bodeguero', 'Bodeguero'),
    ('contador', 'Contador'),
    ('administrador', 'Administrador'),
]

class ModeloAdministrador(models.Model):  # Cambié el nombre de la clase para seguir las convenciones de estilo de Python
    id_usuario = models.AutoField(primary_key=True)  # Si es una clave primaria
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)  # Cambié a EmailField para validación
    contrasena = models.CharField(max_length=100)
    tipo_usuario = models.CharField(max_length=20, choices=OPCIONES_USUARIO)

    class Meta:
        app_label = 'proyectoFerreteria'