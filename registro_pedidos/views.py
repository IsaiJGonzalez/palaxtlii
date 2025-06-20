from django.shortcuts import render, redirect
from firebase_config import fr_db
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import firebase_service as fs
from datetime import datetime, date
import ticket_utils as tk
import subprocess
import os
from django.conf import settings
from core.decorators import gerente_required, ventas_required, cajero_required, login_required



@login_required
def registro_pedidos(request):
    no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
    privilegio = request.session.get("usuario", {}).get("privilegio", 0)  # Si no hay privilegio, asigna 0
    locacion_empleado = request.session.get('usuario',{}).get('sucursal',0)
    caja_activa = fs.consultar_caja_activa(no_emp)

    if not caja_activa :
        return redirect('apertura_caja')

    data_emp = {
        "nombre": request.session.get('usuario', {}).get('nombre', ''),
        "numero_empleado": request.session.get('usuario', {}).get('numero_empleado', 0)
    }

    # Definir la plantilla base según el privilegio
    if privilegio == 1:
        base_template = "menu_gerencial.html"
    elif privilegio == 2:
        base_template = "menu_ventas.html"
    elif privilegio == 3:
        base_template = "menu_cajero.html"


    if (locacion_empleado == 1):
        #Vista Hermosa
        folio = fs.obtener_folio_vh()
        folio_mostrado = folio + 1
        fs.ref_folio_vh().set(folio_mostrado)
        locacion_sucursal = fr_db.child('vistahermosa').child('locacion').get()
    elif(locacion_empleado == 2):
        #Moctezuma
        folio = fs.obtener_folio_mc()
        folio_mostrado = folio + 1
        fs.ref_folio_mc().set(folio_mostrado)
        locacion_sucursal = fr_db.child('moctezuma').child('locacion').get()

    return render(request, "registro_pedidos.html", {"base_template": base_template, 'locacion':locacion_sucursal,'folio':folio_mostrado,'loc_em':locacion_empleado,**data_emp})


#@csrf_exempt
@login_required
def guardar_pedido(request):
    if request.method == "POST":
        try:
            locacion_empleado = request.session.get('usuario',{}).get('sucursal',0)
            no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
            data = json.loads(request.body)
            gran_total = data.get('gran_total')
            id_corte = fs.consultar_id_corte_caja_emp(no_emp)
            anticipo = data.get('anticipo')
            metodo_pago = data.get('metodo_pago')
            


            if gran_total == 0 :
                restante_pagado = True
            elif gran_total > 0 :
                restante_pagado = False

            # Llamada a la función de firebase_service correctamente
            fs.registrar_pedido(
                folio=data.get("folio"),
                fecha_registro=data.get('fecha_registro'),
                nombre_cliente=data.get("nombre_cliente"),
                telefono=data.get("telefono"),
                productos=data.get("productos"),
                especificaciones=data.get("especificaciones"),
                forma_entrega=data.get("forma_entrega"),
                metodo_pago=data.get("metodo_pago"),
                total=data.get("total"),
                gran_total=data.get("gran_total"),
                fecha_entrega=data.get('fecha_entrega'),
                hora_entrega=data.get("hora_entrega"),
                anticipo=data.get("anticipo"),
                recibe=data.get("recibe"),
                cel=data.get("cel"),
                direccion=data.get("direccion"),
                referencias=data.get("referencias"),
                costo_envio=data.get("costo_envio"),
                recibido=data.get("recibido"),
                cambio=data.get("cambio"),
                num_operacion=data.get("num_operacion"),
                sucursal=data.get("sucursal"),
                mix_ef=data.get('mix_ef'),
                mix_tar=data.get('mix_tar'),
                at_no_emp=data.get('at_no_emp'),
                at_nom_emp=data.get('at_nom_emp'),
                estado=0,
                restante_pagado=restante_pagado
            )

            if locacion_empleado == 1 and anticipo:
                a = int(anticipo)
                fs.registrar_en_corte_vh(id_corte,'pedido',metodo_pago,a)
            elif locacion_empleado == 2 and anticipo:
                a = int(anticipo)
                fs.registrar_en_corte_mc(id_corte,'pedido',metodo_pago,a)
            try:
                script_path = os.path.join(settings.BASE_DIR,"ticket_utils.py")
                subprocess.Popen([
                    "python", script_path, json.dumps(data), str(locacion_empleado)
                ])
            except Exception as e:
                print("❌ Error al lanzar impresión externa:", e)
            return JsonResponse({
                "success": True
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)