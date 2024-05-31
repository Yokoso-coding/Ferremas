from django import forms
from .models import modeloAdministrador


class modeloAdministradorForm(forms.ModelForm):
    class meta:
     model = modeloAdministrador
     fields = ['id_usuario','nombre','email','contrasena','tipo_usuario']