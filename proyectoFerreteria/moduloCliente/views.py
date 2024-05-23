from django.shortcuts import render
from moduloCliente.models import Producto
from .models import Producto

def home(request):
    return render(request, 'index.html')

def inicio_bodeguero(request):
    # Obtener todos los productos
    productos = Producto.objects.all()
    return render(request, 'inicioBodeguero.html', {'productos': productos})

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'moduloCliente/listar_productos.html', {'productos': productos})
