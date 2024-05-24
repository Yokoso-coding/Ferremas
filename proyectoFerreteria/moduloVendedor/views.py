from django.shortcuts import render
from .models import Producto

# Create your views here.
def vendedor(request):
    Productos = Producto.objects.all()
    return render(request, 'inicioVendedor.html', {'Productos':Productos})