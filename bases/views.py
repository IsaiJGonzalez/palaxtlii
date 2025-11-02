from django.shortcuts import render, redirect
import firebase_service as fs

# Create your views here.

def logout(request):
    request.session.flush()
    print('sesion cerrada')
    return redirect('login')


def base_gerencial(request):
    nombre_empleado = request.session.get('usuario',{}).get('nombre','usuario')
    empleado = request.session.get('usuario',{}).get('numero_empleado',0)
    caja_activa = fs.consultar_caja_activa(empleado)
    return render(request, 'base_gerencial.html' ,{
        'nombre_empleado':nombre_empleado,
        'caja_activa':caja_activa
    })

def cambiar_locacion(request):
    if request.method == 'POST':
        no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
        locacion = int(request.POST.get('locacion'))
        print('no: ',no_emp)
        print('loca: ',locacion)
        fs.cambiar_locacion_empleado(no_emp,locacion)
        request.session.flush()
        print('sesion cerrada')
        return redirect('login')
    