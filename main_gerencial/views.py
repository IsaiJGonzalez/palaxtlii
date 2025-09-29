from django.shortcuts import render,redirect
from firebase_config import fr_db
import firebase_service as fs
from datetime import datetime
import json
from django.http import JsonResponse
from core.decorators import gerente_required, ventas_required, cajero_required, login_required


@gerente_required
def main_gerencial(request):
    empleado = request.session.get('usuario',{}).get('numero_empleado',0)
    caja_activa = fs.consultar_caja_activa(empleado)

    if not caja_activa:
        return redirect('apertura_caja')
    nombre_empleado = request.session.get("usuario",{}).get('nombre', 'Usuario')
    sucursal_empleado = request.session.get('usuario',{}).get('sucursal', 0)
    loc = fs.consultar_sucursal(sucursal_empleado)
    productos_vh = list(fs.obtener_productos_vh().values()) if fs.obtener_productos_vh() else []
    productos_mc = list(fs.obtener_productos_moctezuma().values()) if fs.obtener_productos_moctezuma() else []

    raw_pedidos = fs.obtener_pedidos()
    pedidos = list(raw_pedidos.values()) if raw_pedidos else []
    hoy = datetime.today().date()
    pedidos_hoy = []

    for pedido in pedidos:
        
        #sucursal
        sucursal_ped = pedido.get('sucursal')
        pd_str = pedido.get('fecha_entrega')

        if not sucursal_ped or not sucursal_ped.isdigit():
            continue  # Si está vacío o no es numérico, saltamos el pedido
        
        sucursal_pedido = int(sucursal_ped)
        #Filtramos para que únicamente me de los pedidos
        #que se entregan en la sucursal del usuario

        if sucursal_empleado == sucursal_pedido:
            if pd_str:
                pd_date = datetime.strptime(pd_str,"%Y-%m-%d").date()
            if pd_date == hoy:
                pedidos_hoy.append(pedido)

    

    ventasmc = fs.consultar_ventas_mc() or []
    ventasvh = fs.consultar_ventas_vh() or []



    context = {
            'nombre_empleado': nombre_empleado,
            'prvh':productos_vh,
            'prmc':productos_mc,
            'pedidos':pedidos_hoy,
            'loc':loc,
            'ventasvh' : ventasvh,
            'ventasmc' : ventasmc,
    }

    return render(request, 'menu_gerencial.html', context)



def actualizar_pedido_estado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folio = data.get('folio')
            
            resultado = fs.act_pedido_estado(folio)  # Ejecuta la función
            return JsonResponse({'mensaje': resultado})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Envía error como JSON
    return JsonResponse({'error': 'Método no permitido'}, status=405)
