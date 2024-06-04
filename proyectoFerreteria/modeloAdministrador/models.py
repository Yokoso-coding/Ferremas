from django.db import models

# Create your models here.

OPCIONES_USUARIO=[
    ('Cliente','Vendedor','Bodeguero','Contador','Administrador')
]
class modeloAdministrador(models.Model):
    id_usuario=models.IntegerField
    nombre=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    contrasena=models.CharField(max_length=100)
    tipo_usuario=models.CharField(max_length=20, choices=OPCIONES_USUARIO)

class Meta:
        app_label = 'proyectoFerreteria'