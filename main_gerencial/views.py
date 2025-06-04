from django.shortcuts import render
from firebase_config import fr_db
import firebase_service as fs
from datetime import datetime

# Create your views here.
def main_gerencial(request):
    nombre_empleado = request.session.get("usuario",{}).get('nombre', 'Usuario')
    sucursal_empleado = request.session.get('usuario',{}).get('sucursal','0')
    productos_vh = list(fs.obtener_productos_vh().values()) if fs.obtener_productos_vh() else []
    productos_mc = list(fs.obtener_productos_moctezuma().values()) if fs.obtener_productos_moctezuma() else []

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
        

    return render(request, 'menu_gerencial.html', {'nombre_empleado': nombre_empleado,'prvh':productos_vh,'prmc':productos_mc,'pedidos':pedidos_hoy})