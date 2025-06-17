from django.shortcuts import render, redirect
import firebase_service as fs


# Create your views here.
def corte_caja(request):
    privilegio = request.session.get('usuario',{}).get('privilegio',0)
    no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
    caja_a = fs.consultar_caja_activa(no_emp)
    if not caja_a:
        return redirect('apertura_caja')
    id_caja = fs.consultar_id_caja_emp(no_emp)

    if privilegio == 1:
        base = 'base_gerencial.html'
    elif privilegio == 2:
        base = 'base_ventas.html'
    elif privilegio == 2:
        base = 'base_cajero.html'

    context = {
        'base':base,
        'id_caja':id_caja
    }
    return render(request,'corte_caja.html',context)