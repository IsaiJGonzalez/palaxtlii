from django.shortcuts import render
from django.http import JsonResponse

from firebase_service import obtener_ventas_por_rango


def visor_ventas(request):

    if request.method == 'POST':

        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')
        sucursal = request.POST.get('sucursal')

        ventas = obtener_ventas_por_rango(
            fecha_inicio,
            fecha_fin,
            sucursal
        )

        ventas_formateadas = []

        for venta in ventas:

            productos = venta.get('productos', [])

            for producto in productos:

                fila = {
                    'no_venta': venta.get('no_venta', ''),
                    'fecha_venta': venta.get('fecha_venta', ''),
                    'at_nom_emp': venta.get('at_nom_emp', ''),
                    'productoNombre': producto.get('productoNombre', ''),
                    'cantidad': producto.get('cantidad', 0),
                    'precio_unitario': producto.get('precio_unitario', 0),
                    'subtotal': producto.get('subtotal', 0),
                    'total': venta.get('total', 0),
                    'metodo_pago': venta.get('metodo_pago', ''),
                    'ubicacion': venta.get('ubicacion', ''),
                }

                ventas_formateadas.append(fila)

        return JsonResponse({
            'success': True,
            'ventas': ventas_formateadas
        })

    return render(request, 'visor_ventas.html')