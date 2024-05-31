from django.shortcuts import render
from .forms import modeloAdministradorForm

def crear_usuario(request)
    if request.method == 'POST':
        form =modeloAdministradorForm(request.POST)
        if form.is_valid():
            form.save
            return redirect('administrador/')
        else:
            form = modeloAdministradorForm()
        return render(request,'inicio-admin.html',{'form':form})

# Create your views here.
