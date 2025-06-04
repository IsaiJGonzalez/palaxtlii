from django.shortcuts import render

# Create your views here.
def menu_ventas(request):
    return render(request,'menu_ventas.html')