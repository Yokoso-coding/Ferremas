# Generated by Django 5.0.1 on 2024-07-11 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moduloCliente', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='contrasena',
        ),
    ]