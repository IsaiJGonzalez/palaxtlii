from django.shortcuts import render,redirect 
from django.http import JsonResponse
import firebase_service as fs
import ticket_retiros as tk

# Create your views here.


def retiros(request):

    #validando caja activa
    no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
    sucursal_emp = request.session.get('usuario',{}).get('sucursal',0)
    caja_activa = fs.consultar_caja_activa(no_emp)
    id_apertura = fs.consultar_id_caja_emp(no_emp)
    id_corte = fs.consultar_id_corte_caja_emp(no_emp)
    #monto_en_caja = fs.consultar_monto_en_caja(id_corte,sucursal_emp)

    if not caja_activa: #retorna a la apertura si no hay caja para hacer un retiro
        return redirect('apertura_caja')
    
    #variables globales para la función
    privilegio = request.session.get('usuario',{}).get('privilegio',0)

    if privilegio == 1:
        base = 'base_gerencial.html'
    elif privilegio == 2:
        base = 'base_ventas.html'
    elif privilegio == 3:
        base = 'base_cajero.html'
    else:
        return
    
    context = {
        'base':base,
        'no_emp':no_emp,
        'id_apertura' : id_apertura,
        #'monto_en_caja' : monto_en_caja,
    }


    if request.method == 'POST':
        confirmacion = int(request.POST.get('confirmacion'))
        access = fs.consultar_confirmacion(confirmacion)
        retira = request.POST.get('retira')
        existe_empleado = fs.verificar_exis_empleado(retira)
        if not access : 
            return JsonResponse({'error': 'Acceso denegado: Código incorrecto'}, status = 403)
        if not existe_empleado : 
            return JsonResponse({'error': 'Acceso denegado: Empleado ingresado no existente'}, status = 403)
        
        data = {
            'apertura_id' : id_apertura,
            'corte_id' : id_corte,
            'numero_empleado' : no_emp,
            'retira' : int(retira),
            'fecha' : request.POST.get('fecha'),
            'monto' : int(request.POST.get('monto_retiro')),
            'motivo' : request.POST.get('motivo')
        }
        fs.registrar_retiro(sucursal_emp,data)
        tk.imprimir_retiros(sucursal_emp,data)


        print('Retiro registrado')
        return redirect('retiros')

    return render(request,'retiros.html',context)