from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from django.conf import settings
from django.urls import reverse
import uuid
from datetime import datetime
from django.db.models import Q
# Create your views here.
def vendedor(request):
    busqueda = request.GET.get("buscar")
    Productos = Producto.objects.all()
    if busqueda:
        Productos = Producto.objects.filter(
            Q(id_producto__icontains = busqueda) |
            Q(nombre__icontains = busqueda) 
        ).distinct()
    return render(request, 'inicioVendedor.html', {'Productos':Productos})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if str(producto.id) in carrito:
        if carrito[str(producto.id)]['cantidad'] < producto.stock:
            carrito[str(producto.id)]['cantidad'] += 1
        else:
            # Opcional: agregar un mensaje de error o advertencia sobre stock insuficiente
            pass
    else:
        if producto.stock > 0:
            carrito[str(producto.id)] = {'nombre': producto.nombre, 'precio': str(producto.precio), 'cantidad': 1}
        else:
            # Opcional: agregar un mensaje de error o advertencia sobre stock insuficiente
            pass

    request.session['carrito'] = carrito
    return redirect('inicioVendedor')

def reducir_cantidad(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        if carrito[str(producto_id)]['cantidad'] > 1:
            carrito[str(producto_id)]['cantidad'] -= 1
        else:
            del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    return render(request, 'ver_carrito.html', {'carrito': carrito, 'total': total})
