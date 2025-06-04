from django.shortcuts import render, redirect
from django.utils.timezone import now
import pytz
from firebase_config import fr_db
import firebase_service as fs

# Create your views here.
def punto_venta(request):
    
    #Datos de empleado y dirección sucursal
    direccion_empleado = request.session.get('usuario',{}).get('sucursal',0)
    privilegio = request.session.get('usuario',{}).get('privilegio',0)
    nombre_emp = request.session.get('usuario',{}).get('nombre','Desconocido')
    no_emp = request.session.get('usuario',{}).get('numero_empleado',0)


    #Locación y productos de acuerdo al empleado 
    if(direccion_empleado == 1):
        
        direccion_sucursal = fr_db.child('vistahermosa').child('locacion').get()#<------
        
        numero_venta = fr_db.child('seriabilidad').child('vistahermosa').child('venta').get() or 1#<------
        
        productos = list(fs.obtener_productos_vh().values()) if fs.obtener_productos_vh() else []
        
    
    elif(direccion_empleado == 2):
        direccion_sucursal = fr_db.child('moctezuma').child('locacion').get()#<------
    
        numero_venta = fr_db.child('seriabilidad').child('moctezuma').child('venta').get() or 1#<------
    
        productos = list(fs.obtener_productos_moctezuma().values()) if fs.obtener_productos_moctezuma() else []
        
    
    else:
        direccion_sucursal = 'None'
    
    #templates de acuerdo al privilegio
    if privilegio == 1 :
        template = 'base_gerencial.html'
    elif privilegio == 2:
        template = 'base_ventas.html'
    elif privilegio == 3:
        template = 'base_cajero.html'
    else :
        redirect('login')

    
    context = {
        'today_date': now().astimezone(pytz.timezone('America/Mexico_City')).date().isoformat(),
        'numero_venta':numero_venta,
        'direccion_sucursal':direccion_sucursal,
        'template' : template,
        'empleado' : nombre_emp,
        'no_emp' : no_emp,
        'productos' : productos
    }

    return render(request,'punto_venta.html',context)