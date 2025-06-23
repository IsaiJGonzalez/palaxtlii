from django.shortcuts import render
import firebase_service as fs
from firebase_config import fr_db
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.http import JsonResponse
import json
from core.decorators import gerente_required, ventas_required, cajero_required, gerente_ventas_required


def convertir_fecha(fecha_str):
    if isinstance(fecha_str, datetime):
        return fecha_str
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


@gerente_ventas_required
def pedidos(request):
    # --- Parámetros base ---
    fecha_limite = datetime.now() - timedelta(weeks=5)
    orden = request.GET.get('orden', 'entrega')
    tipo = request.GET.get('tipo')  # Para diferenciar si se piden entregados vía fetch
    
    #<-Obtener la plantilla correspondiente al nivel del usuario
    privilegio = request.session.get('usuario',{}).get('privilegio',0)
    if privilegio == 1 :
        base = 'base_gerencial.html'
    elif privilegio == 2:
        base = 'base_ventas.html'
    elif privilegio == 3:
        base = 'base_cajero.html'
    #<----

    # --- Obtener y procesar datos desde Firebase ---
    pedidos = fs.obtener_pedidos()
    pedidos_valores = list(pedidos.values()) if pedidos else []

    for p in pedidos_valores:
        p['fecha_registro'] = convertir_fecha(p.get('fecha_registro', '1900-01-01'))
        p['fecha_entrega'] = convertir_fecha(p.get('fecha_entrega', '1900-01-01'))

    # Filtro dinámico según criterio de orden
    if orden == 'entrega':
        pedidos_recientes = [p for p in pedidos_valores if p['fecha_entrega'] and p['fecha_entrega'] >= fecha_limite]
    else:  # orden == 'registro'
        pedidos_recientes = [p for p in pedidos_valores if p['fecha_registro'] and p['fecha_registro'] >= fecha_limite]

    if orden == 'entrega':
        pedidos_recientes = sorted(pedidos_recientes, key=lambda x: x['fecha_entrega'], reverse=False)
    else:
        pedidos_recientes = sorted(pedidos_recientes, key=lambda x: x['fecha_registro'], reverse=False)

    # --- Separar por estado ---
    pedidos_no_entregados = [p for p in pedidos_recientes if p.get('estado') == 0]
    pedidos_entregados = [p for p in pedidos_recientes if p.get('estado') == 1]

    # --- Paginación para entregados ---
    paginator_entregados = Paginator(pedidos_entregados, 10)
    page_entregados = request.GET.get('page_entregados', 1)

    try:
        pedidos_entregados_pag = paginator_entregados.get_page(page_entregados)
    except:
        pedidos_entregados_pag = paginator_entregados.get_page(1)

    # --- Si es petición AJAX (fetch): responder solo JSON ---
    if request.headers.get("x-requested-with") == "XMLHttpRequest" and tipo == 'entregados':
        pedidos_json = [
            {
                "folio": p.get("folio"),
                "fecha_registro": p.get("fecha_registro").strftime("%d de %B de %Y") if p.get("fecha_registro") else "",
                "nombre_cliente": p.get("nombre_cliente"),
                "fecha_entrega": p.get("fecha_entrega").strftime("%d de %B de %Y") if p.get("fecha_entrega") else "",
            } for p in pedidos_entregados_pag
        ]
        return JsonResponse({'pedidos': pedidos_json})

    # --- Si NO es AJAX: render normal del template ---
    return render(
        request,
        'pedidos.html',
        {
            'pedidos_no_entregados': pedidos_no_entregados,
            'pedidos_entregados': pedidos_entregados_pag,
            'orden': orden,
            'base':base
        },
    )



def act_pedido_estado(request):
    #valores globales
    no_emp = request.session.get('usuario',{}).get('numero_empleado',0)
    caja_activa = fs.consultar_caja_activa(no_emp)
    if not caja_activa:
        return JsonResponse({'Error': 'Caja inactiva'}, status=500)
    corte_id = fs.consultar_id_corte_caja_emp(no_emp)
    if request.method == 'POST':
        try:
            #obteniendo valores globales para la función
            sucursal_emp = request.session.get('usuario',{}).get('sucursal',0)

            #obteniendo la data del json
            data = json.loads(request.body)
            #folio del pedido
            folio = data.get('folio')
            
            #pago seleccionado en caso de haber restante
            pago_seleccionado = data.get('pagoSeleccionado')
            if pago_seleccionado : 
                restante = fs.consultar_restante_pedido(folio)
                if sucursal_emp == 1:
                    fs.registrar_en_corte_vh(corte_id,'pedido',pago_seleccionado,restante)
                elif sucursal_emp == 2:
                    fs.registrar_en_corte_mc(corte_id,'pedido',pago_seleccionado,restante)
            
            resultado = fs.act_pedido_estado(folio)  # Ejecuta la función
            return JsonResponse({'mensaje': resultado})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Envía error como JSON
    return JsonResponse({'error': 'Método no permitido'}, status=405)
