from django.shortcuts import render
import firebase_service as fs

# Create your views here.
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

    print(cortes)
    return render(request,'historial_cajas.html',context)