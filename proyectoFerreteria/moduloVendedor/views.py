from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from django.conf import settings
from django.urls import reverse
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import uuid
from datetime import datetime
from django.db.models import Q
from moduloCliente.models import Producto
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

def busquedaVendedor(request):
    busqueda = request.GET.get("buscar")
    Productos = Producto.objects.all()
    if busqueda:
        Productos = Producto.objects.filter(
            Q(id__icontains = busqueda) |
            Q(nombre__icontains = busqueda) 
        ).distinct()
    return render(request, 'busquedaVendedor.html', {'Productos':Productos})

def catalogoVendedor(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    # Filtrar productos por nombre
    productos = Producto.objects.filter(nombre__icontains=search_query)
    
    # Filtrar productos por categoría si se selecciona una
    if category_id:
        productos = productos.filter(categoria_id=category_id)
    
    categorias = Categoria.objects.all()

    context = {
        'productos': productos,
        'categorias': categorias,
    }
    
    return render(request, 'catalogoVendedor.html', context)

def pedidoVendedor(request):
    return render(request, 'pedidoVendedor.html')

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
    return redirect('catalogo_productos')

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


def iniciar_pago(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())

    # Genera un identificador único para la transacción que no exceda 26 caracteres
    buy_order = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex)[:10]
    session_id = request.session.session_key
    return_url = request.build_absolute_uri(reverse('confirmar_pago'))

    commerce_code = settings.TRANSBANK_COMMERCE_CODE
    api_key = settings.TRANSBANK_API_KEY
    tx = Transaction(WebpayOptions(commerce_code, api_key, settings.TRANSBANK_ENVIRONMENT))

    response = tx.create(buy_order, session_id, total, return_url)
    
    return redirect(response['url'] + '?token_ws=' + response['token'])

def confirmar_pago(request):
    token = request.GET.get('token_ws')
    commerce_code = settings.TRANSBANK_COMMERCE_CODE
    api_key = settings.TRANSBANK_API_KEY
    tx = Transaction(WebpayOptions(commerce_code, api_key, settings.TRANSBANK_ENVIRONMENT))
    response = tx.commit(token)
    
    if response['status'] == 'AUTHORIZED':
        # Actualizar el stock de los productos
        carrito = request.session.get('carrito', {})
        for key, item in carrito.items():
            producto = Producto.objects.get(id=key)
            producto.stock -= item['cantidad']
            producto.save()
        
        # Vaciar el carrito después de la compra
        request.session['carrito'] = {}
        
        return render(request, 'pago_exitoso.html', {'response': response})
    else:
        return render(request, 'pago_fallido.html', {'response': response})