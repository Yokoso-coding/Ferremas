from django.shortcuts import render,redirect,get_object_or_404
from moduloCliente.models import Producto
#from moduloCliente.models import Pedido
from .models import DetalleBodega
from .forms import ProductoForm
from django.db.models import Q
from .models import DetallePedido

#MUESTRA EN INICIOBODEGUERO
def bodeguero(request):
    # Obtener todos los productos por defecto
    productos = Producto.objects.all()

    # Verificar si se ha realizado una búsqueda
    busqueda = request.GET.get("buscar")
    if busqueda:
        # Filtrar los productos basados en la búsqueda
        productos = Producto.objects.filter(
            Q(id_producto__icontains=busqueda) |
            Q(nombre__icontains=busqueda)
        ).distinct()

    return render(request, 'inicioBodeguero.html', {'productos': productos})

#muestra en pedidoBodeguero
def bodeguerop(request):
    detalles = DetalleBodega.objects.all()
    return render(request, 'pedidoBodeguero.html', {'detalles': detalles})



def pedido_bodeguero(request):
    detalles = DetallePedido.objects.all()  
    context = {'detalles': detalles}
    return render(request, 'pedidoBodeguero.html', context)


#CRUD BODEGUERO-PRODUCTOS
def listar_productos(request):
    productos = Producto.objects.all()

    busqueda = request.GET.get("buscar")
    if busqueda:
        productos = Producto.objects.filter(
            Q(id_producto__icontains=busqueda) |
            Q(nombre__icontains=busqueda)
        ).distinct()

    return render(request, 'inicioBodeguero.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'actualizar_producto.html', {'form': form, 'pk': pk})

def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})