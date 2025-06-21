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

    if request.method == 'POST':
        billetes  = {
            '1000' : request.POST.get('billetes_1000'),
            '500' : request.POST.get('billetes_500'),
            '200' : request.POST.get('billetes_200'),
            '100' : request.POST.get('billetes_100'),
            '50' : request.POST.get('billetes_50'),
            '20' : request.POST.get('billetes_20')
        }
        monedas = request.POST.get('monedas')

    return render(request,'corte_caja.html',context)