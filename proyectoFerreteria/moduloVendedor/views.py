from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, DetallePedido, Pedido
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.conf import settings
from django.urls import reverse
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import uuid
from datetime import datetime
from django.db.models import Q
from moduloCliente.models import Producto, Pedido
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
# Create your views here._vendedor
"""
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

def agregar_al_carrito_vendedor(request, producto_id):
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

def reducir_cantidad_vendedor(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        if carrito[str(producto_id)]['cantidad'] > 1:
            carrito[str(producto_id)]['cantidad'] -= 1
        else:
            del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito_vendedor')

def eliminar_del_carrito_vendedor(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito_vendedor')

def ver_carrito_vendedor(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    return render(request, 'ver_carrito.html', {'carrito': carrito, 'total': total})


def iniciar_pago_vendedor(request):
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

def confirmar_pago_vendedor(request):
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

            # Crear y guardar el pedido en la base de datos
            pedido = Pedido(
                producto=producto,
                cantidad=item['cantidad'],
                total=item['cantidad'] * producto.precio,
                buy_order=response['buy_order']
            )
            pedido.save()
        
        # Vaciar el carrito después de la compra
        request.session['carrito'] = {}
        
        # Agregar un mensaje de éxito
        messages.success(request, 'Su compra ha sido realizada con éxito.')
        
        return render(request, 'pago_exitoso_vendedor.html')
    else:
        return render(request, 'pago_fallido_vendedor.html', {'response': response})"""

def home_vendedor(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    request.session['carrito'] = {}
    return render(request, 'index_vendedor.html', context)

class CustomLoginView(LoginView):
    template_name = 'login_vendedor.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('home_vendedor')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home_vendedor')

@login_required
def perfil_cliente_vendedor(request):
    return render(request, 'perfil_cliente_vendedor.html')

@login_required
def config_cliente_vendedor(request):
    user = request.user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil_cliente_vendedor')
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'perfil_cliente_vendedor.html', {'form': form})

def catalogo_productos_vendedor(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    ordenar_por = request.GET.get('ordenar_por', '')

    productos = Producto.objects.all()

    if search_query:
        productos = productos.filter(nombre__icontains=search_query)
    
    if category_filter:
        productos = productos.filter(categoria__id=category_filter)

    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    if ordenar_por:
        if ordenar_por == 'precio_asc':
            productos = productos.order_by('precio')
        elif ordenar_por == 'precio_desc':
            productos = productos.order_by('-precio')

    # Obtener carrito de la sesión
    carrito = request.session.get('carrito', {}).values()
    
    # Calcular el total
    total = sum(item['cantidad'] * item['precio'] for item in carrito)
    
    context = {
        'productos': productos,
        'carrito': carrito,
        'total': total,
        'search_query': search_query,
        'category_filter': category_filter,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'ordenar_por': ordenar_por,
    }
    
    return render(request, 'catalogo_productos_vendedor.html', context)

def agregar_al_carro_vendedor(request, producto_id):
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
            carrito[str(producto.id)] = {
                'producto_id': producto.id, 
                'producto_nombre': producto.nombre, 
                'precio': float(producto.precio),  # Convertir a float
                'cantidad': 1
            }
        else:
            # Opcional: agregar un mensaje de error o advertencia sobre stock insuficiente
            pass

    request.session['carrito'] = carrito
    return redirect('catalogo_productos_vendedor')

def aumentar_cantidad_vendedor(request, key):
    carrito = request.session.get('carrito', {})
    if key in carrito:
        carrito[key]['cantidad'] += 1
        request.session['carrito'] = carrito
    return redirect('ver_carrito_vendedor')

def reducir_cantidad_vendedor(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        if carrito[str(producto_id)]['cantidad'] > 1:
            carrito[str(producto_id)]['cantidad'] -= 1
        else:
            del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito_vendedor')

def eliminar_del_carrito_vendedor(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito_vendedor')

def ver_carrito_vendedor(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    return render(request, 'ver_carrito_vendedor.html', {'carrito': carrito, 'total': total})

def iniciar_pago_vendedor(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())

    # Genera un identificador único para la transacción que no exceda 26 caracteres
    buy_order = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex)[:10]
    session_id = request.session.session_key
    return_url = request.build_absolute_uri(reverse('confirmar_pago_vendedor'))

    commerce_code = settings.TRANSBANK_COMMERCE_CODE
    api_key = settings.TRANSBANK_API_KEY
    tx = Transaction(WebpayOptions(commerce_code, api_key, settings.TRANSBANK_ENVIRONMENT))

    response = tx.create(buy_order, session_id, total, return_url)
    
    return redirect(response['url'] + '?token_ws=' + response['token'])

@login_required
def confirmar_pago_vendedor(request):
    token = request.GET.get('token_ws')
    commerce_code = settings.TRANSBANK_COMMERCE_CODE
    api_key = settings.TRANSBANK_API_KEY
    tx = Transaction(WebpayOptions(commerce_code, api_key, settings.TRANSBANK_ENVIRONMENT))
    response = tx.commit(token)
    
    if response['status'] == 'AUTHORIZED':
        # Obtener el modelo de usuario personalizado
        CustomUser = get_user_model()
        usuario = CustomUser.objects.get(id=request.user.id)

        carrito = request.session.get('carrito', {})

        # Crear el pedido
        pedido = Pedido.objects.create(
            usuario=usuario,
            estado='completado'
        )

        # Actualizar el stock de los productos y crear detalles del pedido
        for key, item in carrito.items():
            producto = Producto.objects.get(id=key)
            producto.stock -= item['cantidad']
            producto.save()

            # Crear el detalle del pedido
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['cantidad'],
                precio=producto.precio
            )
        
        # Vaciar el carrito después de la compra
        request.session['carrito'] = {}
        
        return render(request, 'pago_exitoso_vendedor.html')
    else:
        return render(request, 'pago_fallido_vendedor.html', {'response': response})