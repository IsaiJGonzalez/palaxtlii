from django.shortcuts import render
from core.decorators import gerente_required, ventas_required, cajero_required



# Create your views here.
@ventas_required
def menu_ventas(request):
    return render(request,'menu_ventas.html')