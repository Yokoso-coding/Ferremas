from django.shortcuts import render

# Create your views here.

def contador(request):
    return render(request, 'inicioContador.html')
