from django.shortcuts import render

# Create your views here.
def menu_cajero(request):
    return render(request, 'menu_cajero.html')