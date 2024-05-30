from django.shortcuts import render,redirect
from moduloCliente.models import Producto
from moduloCliente.models import Pedido
from .models import DetalleBodega
from .forms import ProductoForm
#from django.db.models import Q

def bodeguero(request):
   productos = Producto.objects.all()
  # busqueda = request.GET.get("buscar")
   #if busqueda:
    #    Productos = Producto.objects.filter(
     #       Q(id_producto__icontains = busqueda) |
      #      Q(nombre__icontains = busqueda) 
       # ).distinct()
   return render(request, 'inicioBodeguero.html', {'productos': productos})


def listar_detalles_bodega(request):
    detalles = DetalleBodega.objects.all()
    return render(request, 'pedidoBodeguero.html', {'detalles': detalles})

#CRUD DE 
def bodeguerop(request):
    detalles = DetalleBodega.objects.all()
    return render(request, 'pedidoBodeguero.html', {'detalles': detalles})


def listar_productos(request):
    productos = Producto.objects.all()
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
    producto = Producto.objects.get(pk=pk)
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