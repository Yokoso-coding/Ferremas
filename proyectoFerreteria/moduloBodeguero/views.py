from django.shortcuts import render

# Create your views here.
def bodeguero(request):
    return render(request, 'inicioBodeguero.html')