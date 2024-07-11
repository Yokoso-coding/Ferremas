# users/forms.py
from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)
    contrasena2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = Usuario
        fields = ['nom_usuario', 'nombre', 'email', 'contrasena', 'tipo_usuario']

    def clean_contrasena2(self):
        cd = self.cleaned_data
        if cd['contrasena'] != cd['contrasena2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['contrasena2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de Usuario', max_length=100)