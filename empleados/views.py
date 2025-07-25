from django.shortcuts import render, redirect
from firebase_admin import db
from firebase_config import fr_db
import random
from core.decorators import gerente_required
import firebase_service as fs

@gerente_required
def empleados(request):

    empleados_exist = fr_db.child('empleados').get() 
    if empleados_exist and isinstance(empleados_exist, dict):
        empleados_lista = empleados_exist.values()
    else:
        empleados_lista = [] 
        
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        sucursal = request.POST.get('sucursal')
        privilegio = request.POST.get('privilegio')
        numero_empleado = random.randint(10**4, 10**6 - 1)
        contrasena = numero_empleado
        ch_psw = False
        caja_activa = False
        empleado_ref = fr_db.child('empleados').child(str(numero_empleado))
        empleado_ref.set({'numero_empleado': numero_empleado,'contrasena':contrasena ,'nombre' : nombre + ' ' + apellido, 'telefono' : telefono, 'sucursal': int(sucursal), 'privilegio': int(privilegio), 'ch_psw':ch_psw,'caja_activa':caja_activa})
        return redirect('empleados')
    return render(request,'empleados.html', {'empleados':empleados_lista})


def cambiar_contrasena(request):
    if request.method == 'POST':
        no_emp = request.POST.get('ch_emp')
        psw = request.POST.get('contrasena_dos')
        fs.cambiar_contrasena(no_emp,psw)
        return redirect('empleados')
    return