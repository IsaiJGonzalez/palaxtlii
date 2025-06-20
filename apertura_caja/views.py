from django.shortcuts import render, redirect
from django.http import JsonResponse
import firebase_service as fs

# Create your views here.
def apertura_caja(request):
    privilegio = request.session.get('usuario',{}).get('privilegio',0)
    no_empleado = request.session.get('usuario',{}).get('numero_empleado',0)
    sucursal = request.session.get('usuario',{}).get('sucursal',0)
    caja_a = fs.consultar_caja_activa(no_empleado)
    if caja_a:
        return redirect('corte_caja')

    if privilegio == 1:
        base = 'base_gerencial.html'
    elif privilegio == 2:
        base = 'base_ventas.html'
    elif privilegio == 3:
        base = 'base_cajero.html'

    if request.method == 'POST':
        no_emp = int(request.POST.get('id_empleado'))
        fecha = request.POST.get('fecha_asignacion')
        b1000 = int(request.POST.get('billetes_1000') or 0)
        b500 = int(request.POST.get('billetes_500') or 0)
        b200 = int(request.POST.get('billetes_200') or 0)
        b100 = int(request.POST.get('billetes_100') or 0)
        b50 = int(request.POST.get('billetes_50') or 0)
        b20 = int(request.POST.get('billetes_20') or 0)
        monedas = float(request.POST.get('monedas') or 0)
        fondo = float(request.POST.get('fondo_caja') or 0)

        if sucursal == 1:
            fs.apertura_caja_vh(
                no_emp=no_emp,
                fecha_asignacion=fecha,
                b1000=b1000,
                b500=b500,
                b200=b200,
                b100=b100,
                b50=b50,
                b20=b20,
                monedas=monedas,
                fondo_caja=fondo,
                estado=True
            )
            fs.activar_caja_emp(no_empleado)
            apertura_id = fs.consultar_id_caja_emp(no_emp)
            fs.corte_caja_vh(no_emp,apertura_id,fondo)

        elif sucursal == 2:
            fs.apertura_caja_mc(
                no_emp=no_emp,
                fecha_asignacion=fecha,
                b1000=b1000,
                b500=b500,
                b200=b200,
                b100=b100,
                b50=b50,
                b20=b20,
                monedas=monedas,
                fondo_caja=fondo,
                estado=True
            )
            fs.activar_caja_emp(no_empleado)
            apertura_id = fs.consultar_id_caja_emp(no_emp)
            fs.corte_caja_mc(no_emp,apertura_id,fondo)
        else:
            return redirect('login')
        return redirect('apertura_caja')

    context = {
        'base':base,
        'no_empleado':no_empleado
    }
    return render(request,'apertura_caja.html',context)