from django.shortcuts import render
from .models import Producto
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