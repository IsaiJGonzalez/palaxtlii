from django.shortcuts import render
from core.decorators import gerente_required, ventas_required, cajero_required

# Create your views here.

@cajero_required
def menu_cajero(request):
    return render(request, 'menu_cajero.html')