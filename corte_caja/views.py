from django.shortcuts import render, redirect
import firebase_service as fs
import ticket_corte as tk

# Create your views here.
def corte_caja(request):
    privilegio = request.session.get('usuario',{}).get('privilegio',0)
    no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
    nombre_emp = request.session.get('usuario',{}).get('nombre','')
    sucursal = request.session.get('usuario',{}).get('sucursal',0)
    caja_a = fs.consultar_caja_activa(no_emp)
    if not caja_a:
        return redirect('apertura_caja')
    id_caja = fs.consultar_id_caja_emp(no_emp)
    id_corte = fs.consultar_id_corte_caja_emp(no_emp)

    if privilegio == 1:
        base = 'base_gerencial.html'
    elif privilegio == 2:
        base = 'base_ventas.html'
    elif privilegio == 3:
        base = 'base_cajero.html'

    context = {
        'base':base,
        'id_caja':id_caja
    }

    if request.method == 'POST':
        billetes  = {
            '1000' : int(request.POST.get('billetes_1000') or 0),
            '500' : int(request.POST.get('billetes_500') or 0),
            '200' : int(request.POST.get('billetes_200') or 0),
            '100' : int(request.POST.get('billetes_100') or 0),
            '50' : int(request.POST.get('billetes_50') or 0),
            '20' : int(request.POST.get('billetes_20') or 0)
        }
        monedas = float(request.POST.get('monedas') or 0.0)
        fecha_corte = request.POST.get('fecha_corte')

        total_en_billetes = sum(int(denominacion) * cantidad for denominacion, cantidad in billetes.items())
        total_en_caja = float(total_en_billetes + monedas)
        fs.cerrar_cajas(sucursal,no_emp,id_caja,id_corte,fecha_corte,billetes,monedas,total_en_caja)
        #Consultar los datos del corte al cerrar para impresión del ticket
        data = fs.consultar_corte(sucursal,id_corte)
        tk.imprimir_corte(data,nombre_emp,sucursal)

        return redirect('apertura_caja')

    return render(request,'corte_caja.html',context)