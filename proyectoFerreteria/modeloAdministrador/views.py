from django.shortcuts import render, redirect
from .forms import ModeloAdministradorForm

def crear_usuario(request):
    if request.method == 'POST':
        form = ModeloAdministradorForm(request.POST)
        if form.is_valid():
            form.save()  # Asegúrate de llamar a form.save() con paréntesis
            return redirect('redireccion')
    else:
        form = ModeloAdministradorForm()  # Mueve esta línea fuera del bloque else
    return render(request, 'inicio-admin.html', {'form': form})  # Asegúrate de que esta línea esté fuera del bloque if-else

def redireccion(request):
    return render(request, 'redireccion.html')
