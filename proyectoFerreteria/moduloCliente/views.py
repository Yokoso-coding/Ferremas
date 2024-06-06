from django.shortcuts import render
from moduloCliente.models import Producto
from .models import Producto

def home(request):
    return render(request, 'index.html')

def catalogo_productos(request):
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
            carrito[str(producto.id)] = {'nombre': producto.nombre, 'precio': str(producto.precio), 'cantidad': 1}
        else:
            # Opcional: agregar un mensaje de error o advertencia sobre stock insuficiente
            pass

    request.session['carrito'] = carrito
    return redirect('catalogo_productos')

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'moduloCliente/listar_productos.html', {'productos': productos})
