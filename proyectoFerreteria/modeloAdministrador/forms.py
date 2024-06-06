from django import forms
from .models import ModeloAdministrador

class ModeloAdministradorForm(forms.ModelForm):  # Asegúrate de que el nombre de la clase coincida con el modelo
    class Meta:
        model = ModeloAdministrador
        fields = ['id_usuario', 'nombre', 'email', 'contrasena', 'tipo_usuario']