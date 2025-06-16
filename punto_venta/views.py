from django.shortcuts import render, redirect
from django.utils.timezone import now
import pytz
from firebase_config import fr_db
import firebase_service as fs
from django.http import JsonResponse
from datetime import date
import json
import ticket_venta as tv
from core.decorators import gerente_required, ventas_required, cajero_required, login_required


# Create your views here.
@login_required
def punto_venta(request):
    #Datos de empleado y dirección sucursal
    direccion_empleado = request.session.get('usuario',{}).get('sucursal',0)
    privilegio = request.session.get('usuario',{}).get('privilegio',0)
    nombre_emp = request.session.get('usuario',{}).get('nombre','Desconocido')
    no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
    caja_activa = request.session.get('usuario',{}).get('caja_activa',False)
    if not caja_activa :
        return redirect('apertura_caja')

    #Locación y productos de acuerdo al empleado 
    if(direccion_empleado == 1):
        
        direccion_sucursal = fr_db.child('vistahermosa').child('locacion').get()#<------
        
        numero_venta = fs.obtener_seriabilidad_vh()#<------
        n_venta_m = numero_venta + 1
        fs.ref_seriabilidad_vh().set(n_venta_m)


        productos = list(fs.obtener_productos_vh().values()) if fs.obtener_productos_vh() else []
        
    
    elif(direccion_empleado == 2):
        direccion_sucursal = fr_db.child('moctezuma').child('locacion').get()#<------
    
        numero_venta = fs.obtener_seriabilidad_mc()#<------
        n_venta_m = numero_venta + 1
        fs.ref_seriabilidad_mc().set(n_venta_m)

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



@login_required
def registrar_venta(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        usuario = request.session.get('usuario', {})
        direccion_empleado = request.session.get('usuario',{}).get('sucursal',0)
        nombre_emp = usuario.get('nombre', 'Desconocido')
        no_emp = usuario.get('numero_empleado', 0)
        
        fecha = date.today().isoformat()
        resumen_data = json.loads(request.POST.get('resumen_data', '[]'))
        total = sum(float(p['subtotal']) for p in resumen_data)

        metodo_pago = request.POST.get('metodo_pago')
        recibido = int(request.POST.get('recibido'))
        cambio = int(request.POST.get('cambio'))
        operacion = request.POST.get('numero_operacion')

        if direccion_empleado == 1:
            no_venta = fs.obtener_seriabilidad_vh()
            direccion_sucursal = fr_db.child('vistahermosa').child('locacion').get()

            for producto in resumen_data:
                producto_id = producto.get('productoId')
                cantidad = producto.get('cantidad')
                fs.restar_producto_vh(producto_id,cantidad)

            fs.registrar_venta_vh(
                ubicacion=direccion_sucursal,
                fecha_venta=fecha,
                no_venta=no_venta,
                at_nom_emp=nombre_emp,
                at_no_emp=no_emp,
                productos=resumen_data,
                total=total,
                metodo_pago=metodo_pago,
                recibido=recibido,
                cambio=cambio,
                no_operacion=operacion
            )
            resumen = {
                "ubicacion": direccion_sucursal,
                "fecha_venta": fecha,
                "no_venta": no_venta,
                "at_nom_emp": nombre_emp,
                "at_no_emp": no_emp,
                "productos": resumen_data,
                "total": total,
                "metodo_pago": metodo_pago,
                "recibido": recibido,
                "cambio": cambio,
                "no_operacion": operacion,
                'loc_emp':direccion_empleado
            }
            tv.imprimir_venta(resumen=resumen) 

        elif direccion_empleado == 2:
            no_venta = fs.obtener_seriabilidad_mc()
            direccion_sucursal = fr_db.child('moctezuma').child('locacion').get()#<------
            
            for producto in resumen_data:
                producto_id = producto.get('productoId')
                cantidad = producto.get('cantidad')
                fs.restar_producto_mc(producto_id,cantidad)

            fs.registrar_venta_mc(
                ubicacion=direccion_sucursal,
                fecha_venta=fecha,
                no_venta=no_venta,
                at_nom_emp=nombre_emp,
                at_no_emp=no_emp,
                productos=resumen_data,
                total=total,
                metodo_pago=metodo_pago,
                recibido=recibido,
                cambio=cambio,
                no_operacion=operacion
            )

            resumen = {
                "ubicacion": direccion_sucursal,
                "fecha_venta": fecha,
                "no_venta": no_venta,
                "at_nom_emp": nombre_emp,
                "at_no_emp": no_emp,
                "productos": resumen_data,
                "total": total,
                "metodo_pago": metodo_pago,
                "recibido": recibido,
                "cambio": cambio,
                "no_operacion": operacion,
                'loc_emp':direccion_empleado
            }
            tv.imprimir_venta(resumen=resumen)
            
        else:
            return JsonResponse({'error': 'Empleado sin sucursal válida'}, status=400)

        return redirect('punto_venta')

    except Exception as e:
        print("Error al registrar venta:", e)
        return JsonResponse({'error': 'Ocurrió un error al registrar la venta'}, status=500)