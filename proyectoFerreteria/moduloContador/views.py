from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from .models import Pedido, DetallePedido
# Create your views here.

def contador(request):
    return render(request, 'inicioContador.html')


def reporte_view(request):
    # Obtener todos los pedidos y sus detalles
    pedidos = Pedido.objects.all().select_related('id_usuario')
    detalles = DetallePedido.objects.all().select_related('id_producto', 'id_pedido')

    # Pasar los datos a la plantilla
    data = {
        'pedidos': pedidos,
        'detalles': detalles,
    }

    return render(request, 'inicioContador.html', data)

def generar_pdf(request):
    # Obtener todos los pedidos y sus detalles
    pedidos = Pedido.objects.all().select_related('id_usuario')
    detalles = DetallePedido.objects.all().select_related('id_producto', 'id_pedido')

    # Pasar los datos a la plantilla
    data = {
        'pedidos': pedidos,
        'detalles': detalles,
    }

    # Cargar la plantilla y renderizarla con datos
    template = get_template('reporte_pdf.html')
    html = template.render(data)

    # Generar el PDF
    pdf = HTML(string=html).write_pdf()

    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
    return response