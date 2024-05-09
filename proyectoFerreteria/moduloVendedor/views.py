from django.shortcuts import render

def vendedor(request):
    return render(request, 'inicioVendedor.html')
