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
        print('DIRECCIÓN DEL EMPLEADO: ', direccion_empleado)
        corte_id = request.POST.get('corte')
        venta = int(request.POST.get('venta') or 0)
        fecha = request.POST.get('fecha') or ''
        metodo = request.POST.get('metodo') or ''
        empleado_nombre = request.POST.get('empleado_nombre') or ''
        empleado_numero = request.POST.get('empleado_numero') or ''
        ubicacion = request.POST.get('ubicacion') or ''
        operacion = request.POST.get('operacion') or ''
        total = float( request.POST.get('total')  or 0.0 )
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
                'nombre': nombres[i],
                'cantidad': cantidades[i],
                'precio_unitario': precios[i],
                'subtotal': subtotales[i],
            })


        resumen = {
                "ubicacion":ubicacion,
                "fecha_venta": fecha,
                "no_venta": venta,
                "at_nom_emp": empleado_nombre,
                "at_no_emp": empleado_numero,
                "productos": resumen_data,
                "total": total,
                "metodo_pago": metodo,
                "recibido": recibido,
                "cambio": cambio,
                "no_operacion": operacion,
                'loc_emp':direccion_empleado,
                "mix_ef" : mix_efectivo,
                "mix_tar" : mix_tarjeta
            }
        tr.imprimir_venta(resumen)

        return redirect('ver_ventas', id=corte_id)

    return redirect('ver_ventas', id='default')  # fallback
