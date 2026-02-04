from django.shortcuts import render, redirect
import firebase_service as fs
from core.decorators import login_required, gerente_required
import ticker_reimpreso as tr

# Create your views here.

@gerente_required
def historial_caja(request):

    sucursal = request.session.get('usuario',{}).get('sucursal')
    raw_aperturas = fs.consultar_aperturas(sucursal)
    aperturas = list(raw_aperturas.values())[::-1] if raw_aperturas else []

    raw_cortes = fs.consultar_cortes(sucursal)
    cortes = list(raw_cortes.values())[::-1] if raw_cortes else []

    context = {
        'aperturas' : aperturas,
        'cortes' : cortes,
        'suc' : sucursal
    }

    return render(request,'historial_cajas.html',context)

@login_required
def ver_ventas(request,id):
    sucursal = request.session.get('usuario',{}).get('sucursal')
    # Se asume que fs.consultar_venta_historica ya trae los campos nuevos de la BD
    raw_venta_historica = fs.consultar_venta_historica(id,sucursal)
    venta_historica = raw_venta_historica[::-1]
    context = {
        'v_h' : venta_historica,
        'corte_id' : id
    }
    return render(request, 'ver_ventas.html',context)


def imprimir_ticket(request):

    if request.method == 'POST':
        direccion_empleado = request.session.get('usuario',{}).get('sucursal',0)
        
        corte_id = request.POST.get('corte')
        venta = int(request.POST.get('venta') or 0)
        fecha = request.POST.get('fecha') or ''
        metodo = request.POST.get('metodo') or ''
        empleado_nombre = request.POST.get('empleado_nombre') or ''
        empleado_numero = request.POST.get('empleado_numero') or ''
        ubicacion = request.POST.get('ubicacion') or ''
        operacion = request.POST.get('operacion') or ''
        
        total = float( request.POST.get('total')  or 0.0 )
        
        # --- NUEVOS CAMPOS DE DESCUENTO ---
        descuento_monto = float(request.POST.get('descuento_monto') or 0.0)
        info_descuento = request.POST.get('info_descuento') or 'Ninguno'
        # ----------------------------------

        mix_tarjeta = float(request.POST.get('mix_tarjeta')  or 0.0 )
        mix_efectivo = float(request.POST.get('mix_efectivo')  or 0.0)
        recibido = float(request.POST.get('recibido')  or 0.0)
        cambio = float(request.POST.get('cambio')  or 0.0) 
        
        nombres = request.POST.getlist('productos_nombre[]')
        cantidades = request.POST.getlist('productos_cantidad[]')
        precios = request.POST.getlist('productos_precio_unitario[]')
        subtotales = request.POST.getlist('productos_subtotal[]')
        
        resumen_data = []
        for i in range(len(nombres)):
            resumen_data.append({
                'nombre': nombres[i], # Ojo: en ticket_venta a veces espera 'productoNombre' o lo busca por ID. 
                # Si tu ticket usa ID, esto es solo visual si falla la busqueda.
                # Pero para reimpresión simple suele bastar.
                'cantidad': cantidades[i],
                'precio_unitario': precios[i],
                'subtotal': subtotales[i],
                # Agregamos dummy ID si el ticket lo exige estrictamente, 
                # o asegúrate que tu ticket_venta maneje falta de ID si solo imprimes texto.
                'productoId': '0' 
            })


        resumen = {
                "ubicacion":ubicacion,
                "fecha_venta": fecha,
                "no_venta": venta,
                "at_nom_emp": empleado_nombre,
                "at_no_emp": empleado_numero,
                "productos": resumen_data,
                "total": total,
                
                # --- AGREGAMOS AL RESUMEN ---
                "descuento_monto": descuento_monto,
                "info_descuento": info_descuento,
                # ----------------------------

                "metodo_pago": metodo,
                "recibido": recibido,
                "cambio": cambio,
                "no_operacion": operacion,
                'loc_emp':direccion_empleado,
                "mix_ef" : mix_efectivo,
                "mix_tar" : mix_tarjeta
            }
        
        # Importante: tr debe estar importado arriba como 'import ticket_venta as tr'
        tr.imprimir_venta(resumen)

        return redirect('ver_ventas', id=corte_id)

    return redirect('ver_ventas', id='default')