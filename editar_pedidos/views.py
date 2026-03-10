import json
from django.shortcuts import render
from django.http import JsonResponse

import firebase_service as fs


# ==============================
# Página principal
# ==============================

def editar_pedido_page(request):
    return render(request, "editar_pedido.html")


# ==============================
# Obtener folios activos
# ==============================

def api_folios(request):
    data = fs.obtener_folios_activos()
    return JsonResponse({"folios": data})


# ==============================
# Obtener pedido por ID
# ==============================

def api_pedido(request, pedido_id):
    pedido = fs.obtener_pedido_por_id(pedido_id)

    if not pedido:
        return JsonResponse({"ok": False})

    return JsonResponse({"ok": True, "pedido": pedido})


# ==============================
# Editar pedido
# ==============================

def api_editar_pedido(request, pedido_id):

    if request.method != "POST":
        return JsonResponse({"ok": False})

    usuario = request.session.get('usuario', {})
    nombre_emp = usuario.get('nombre', 'Desconocido')

    data = json.loads(request.body)

    res = fs.editar_pedido(pedido_id, data, nombre_emp)

    return JsonResponse(res)
