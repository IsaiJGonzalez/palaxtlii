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
    # Datos de empleado y sesión
    usuario = request.session.get('usuario', {})
    direccion_empleado = usuario.get('sucursal', 0)
    privilegio = usuario.get('privilegio', 0)
    nombre_emp = usuario.get('nombre', 'Desconocido')
    no_emp = usuario.get('numero_empleado', 0)
    
    # Verificar caja activa
    caja_activa = fs.consultar_caja_activa(no_emp)
    if not caja_activa:
        return redirect('apertura_caja')
    
    # 1. OBTENER TARJETAS GLOBALES (CORRECCIÓN AQUÍ)
    # Se obtienen de la raíz, sin importar la sucursal del empleado
    tarjetas_descuento = fs.obtener_tarjetas_descuento()
    
    # Locación y productos según sucursal
    productos = []
    direccion_sucursal = 'None'
    numero_venta = 0

    if direccion_empleado == 1:
        direccion_sucursal = fr_db.child('vistahermosa').child('locacion').get()
        numero_venta = fs.obtener_seriabilidad_vh()
        # Actualizar seriabilidad (ojo: esto incrementa el contador solo con entrar a la vista, 
        # considera moverlo al momento de guardar venta si prefieres no saltar folios)
        fs.ref_seriabilidad_vh().set(numero_venta + 1)
        productos = list(fs.obtener_productos_vh().values()) if fs.obtener_productos_vh() else []
        
    elif direccion_empleado == 2:
        direccion_sucursal = fr_db.child('moctezuma').child('locacion').get()
        numero_venta = fs.obtener_seriabilidad_mc()
        fs.ref_seriabilidad_mc().set(numero_venta + 1)
        productos = list(fs.obtener_productos_moctezuma().values()) if fs.obtener_productos_moctezuma() else []
    
    # Templates según privilegio
    if privilegio == 1:
        template = 'base_gerencial.html'
    elif privilegio == 2:
        template = 'base_ventas.html'
    elif privilegio == 3:
        template = 'base_cajero.html'
    else:
        return redirect('login')

    # Convertir tarjetas a JSON para pasarlas al JS
    tarjetas_json = json.dumps(tarjetas_descuento)

    context = {
        'today_date': now().astimezone(pytz.timezone('America/Mexico_City')).date().isoformat(),
        'numero_venta': numero_venta,
        'direccion_sucursal': direccion_sucursal,
        'template': template,
        'empleado': nombre_emp,
        'no_emp': no_emp,
        'productos': productos,
        'tarjetas_json': tarjetas_json  # <--- Pasamos las tarjetas globales
    }

    return render(request, 'punto_venta.html', context)


def registrar_venta(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        # Datos de sesión
        usuario = request.session.get('usuario', {})
        direccion_empleado = usuario.get('sucursal', 0)
        nombre_emp = usuario.get('nombre', 'Desconocido')
        no_emp = usuario.get('numero_empleado', 0)
        id_corte = fs.consultar_id_corte_caja_emp(no_emp)

        # Datos Generales
        fecha = date.today().isoformat()
        resumen_data = json.loads(request.POST.get('resumen_data', '[]'))
        
        # --- CORRECCIÓN 1: BLINDAJE DE VALORES NUMÉRICOS ---
        # Si el input viene vacío (''), usa 0.
        total_final = float(request.POST.get('total_venta_final') or 0)
        descuento_monto = float(request.POST.get('descuento_monto') or 0)
        info_descuento = request.POST.get('info_descuento', 'Ninguno')
        
        metodo_pago = request.POST.get('metodo_pago')
        
        # Aquí tronaba: Ahora si viene vacío, toma 0
        recibido = float(request.POST.get('recibido') or 0)
        cambio = float(request.POST.get('cambio') or 0)
        mix_ef = float(request.POST.get('mix_ef') or 0)
        mix_tar = float(request.POST.get('mix_tar') or 0)
        
        operacion = request.POST.get('numero_operacion', '')
        ticket = int(request.POST.get('ticket') or 0)

        # --- CORRECCIÓN 2: DESCONTAR STOCK TARJETA ---
        # Se obtiene el código del input hidden que agregamos
        codigo_tarjeta = request.POST.get('codigo_tarjeta_usada')
        
        if codigo_tarjeta and codigo_tarjeta.strip() != '':
            # Llamamos a la función de firebase_service para restar 1
            fs.restar_uso_tarjeta(codigo_tarjeta)
            print(f"Descontada existencia de tarjeta: {codigo_tarjeta}")

        # Preparar Resumen Base
        resumen_base = {
            "fecha_venta": fecha,
            "at_nom_emp": nombre_emp,
            "at_no_emp": no_emp,
            "productos": resumen_data,
            "total": total_final,
            "descuento_monto": descuento_monto,
            "info_descuento": info_descuento,
            "metodo_pago": metodo_pago,
            "recibido": recibido,
            "cambio": cambio,
            "no_operacion": operacion,
            'loc_emp': direccion_empleado,
            "mix_ef": mix_ef,
            "mix_tar": mix_tar
        }

        # Estructura para el corte
        if metodo_pago == "mixto":
            total_corte = {'e': mix_ef, 't': mix_tar}
        else:
            total_corte = total_final

        # --- LÓGICA POR SUCURSAL ---
        if direccion_empleado == 1: # Vista Hermosa
            no_venta = fs.obtener_seriabilidad_vh()
            direccion_sucursal = fr_db.child('vistahermosa').child('locacion').get()
            
            for producto in resumen_data:
                fs.restar_producto_vh(producto.get('productoId'), producto.get('cantidad'))

            fs.registrar_venta_vh(
                ubicacion=direccion_sucursal, fecha_venta=fecha, no_venta=no_venta,
                at_nom_emp=nombre_emp, at_no_emp=no_emp, productos=resumen_data,
                total=total_final, metodo_pago=metodo_pago, recibido=recibido,
                cambio=cambio, no_operacion=operacion, mix_ef=mix_ef, mix_tar=mix_tar,
                descuento_aplicado=descuento_monto, info_descuento=info_descuento
            )

            resumen_base.update({"ubicacion": direccion_sucursal, "no_venta": no_venta})
            fs.registrar_en_corte_vh(id_corte, 'venta', metodo_pago, total_corte, resumen_base)

            if ticket == 1: tv.imprimir_venta(resumen=resumen_base)

        elif direccion_empleado == 2: # Moctezuma
            no_venta = fs.obtener_seriabilidad_mc()
            direccion_sucursal = fr_db.child('moctezuma').child('locacion').get()

            for producto in resumen_data:
                fs.restar_producto_mc(producto.get('productoId'), producto.get('cantidad'))

            fs.registrar_venta_mc(
                ubicacion=direccion_sucursal, fecha_venta=fecha, no_venta=no_venta,
                at_nom_emp=nombre_emp, at_no_emp=no_emp, productos=resumen_data,
                total=total_final, metodo_pago=metodo_pago, recibido=recibido,
                cambio=cambio, no_operacion=operacion, mix_ef=mix_ef, mix_tar=mix_tar,
                descuento_aplicado=descuento_monto, info_descuento=info_descuento
            )

            resumen_base.update({"ubicacion": direccion_sucursal, "no_venta": no_venta})
            fs.registrar_en_corte_mc(id_corte, 'venta', metodo_pago, total_corte, resumen_base)

            if ticket == 1: tv.imprimir_venta(resumen=resumen_base)
        else:
            return JsonResponse({'error': 'Empleado sin sucursal válida'}, status=400)

        return redirect('punto_venta')

    except Exception as e:
        print("Error CRÍTICO al registrar venta:", e) # Ver esto en consola
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)