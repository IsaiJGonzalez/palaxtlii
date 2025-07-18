from django.shortcuts import render
from core.decorators import gerente_required, ventas_required, cajero_required
import firebase_service as fs
from datetime import datetime
import ticket_prueba as tk_pr


# Create your views here.
@ventas_required
def menu_ventas(request):
    sucursal_empleado = request.session.get('usuario',{}).get('sucursal', 0)
    loc = fs.consultar_sucursal(sucursal_empleado)
    pedidos = list(fs.obtener_pedidos().values())
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

    context = {
            'pedidos':pedidos_hoy,
            'loc':loc,
    }
    return render(request,'menu_ventas.html',context)