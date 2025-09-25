from django.shortcuts import render
import firebase_service as fs
from core.decorators import login_required, gerente_required

# Create your views here.

@gerente_required
def historial_caja(request):

    sucursal = request.session.get('usuario',{}).get('sucursal')
    raw_aperturas = fs.consultar_aperturas(sucursal)
    aperturas = list(raw_aperturas.values())[::-1] if raw_aperturas else []

    raw_cortes = fs.consultar_cortes(sucursal)
    cortes = list(raw_cortes.values())[::-1] if raw_cortes else []

    context = {
        'aperturas' : aperturas,
        'cortes' : cortes
    }

    return render(request,'historial_cajas.html',context)


@login_required
def ver_ventas(request,id):
    sucursal = request.session.get('usuario',{}).get('sucursal')
    venta_historica = fs.consultar_venta_historica(id,sucursal)
    context = {
        'v_h' : venta_historica
    }
    return render(request, 'ver_ventas.html',context)