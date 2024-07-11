from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import uuid
from datetime import datetime

def home(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    request.session['carrito'] = {}
    return render(request, 'index.html', context)

def registrar_cliente(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.contrasena = make_password(form.cleaned_data['contrasena'])
            new_user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registro.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = 'login'

@login_required
def perfil_cliente(request):
    return render(request, 'profile.html')

@login_required
def config_cliente(request):
    user = request.user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'users/settings.html', {'form': form})

def catalogo_productos(request):
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
    
    return render(request, 'catalogo_productos.html', context)

def agregar_al_carro(request, producto_id):
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
    return redirect('catalogo_productos')

def aumentar_cantidad(request, key):
    carrito = request.session.get('carrito', {})
    if key in carrito:
        carrito[key]['cantidad'] += 1
        request.session['carrito'] = carrito
    return redirect('ver_carrito')

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

