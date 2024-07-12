# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nom_usuario', 'nombre', 'email', 'password1', 'password2', 'tipo_usuario']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError('Las contraseñas no coinciden')
        return cd['password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de Usuario', max_length=100)