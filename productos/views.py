from django.shortcuts import render, redirect
from firebase_config import fr_db
import firebase_service as fs
import json
from django.http import JsonResponse
from core.decorators import gerente_required, ventas_required, cajero_required, gerente_ventas_required


# Create your views here.
@gerente_ventas_required
def productos(request):
    productos_vh = list(fs.obtener_productos_vh().values()) if fs.obtener_productos_vh() else []
    productos_mc = list(fs.obtener_productos_moctezuma().values()) if fs.obtener_productos_moctezuma() else []
    categorias_r = fr_db.child('categorias').get()
    privilegio = request.session.get('usuario',{}).get('privilegio')

    #templates de acuerdo al privilegio
    if privilegio == 1 :
        template = 'base_gerencial.html'
    elif privilegio == 2:
        template = 'base_ventas.html'
    elif privilegio == 3:
        template = 'base_cajero.html'
    else :
        redirect('login')

    if categorias_r:
        categorias = [{"id": k, "nombre": v["nombre"]} for k, v in categorias_r.items()]
    else:
        categorias = []

    if (request.method == 'POST'):
            #atributos
        nombre = request.POST.get('nombre')
        existencias_str = request.POST.get('existencias')
        existencias = int(existencias_str) if existencias_str and existencias_str.isdigit() else None
        precio = int(request.POST.get('precio'))
        categoria = request.POST.get('categoria')
        estado = True if request.POST.get('estado') == 'on' else False
        punto_reorden = int(request.POST.get('punto_reorden'))
        ingredientes_json = request.POST.get('ingredientes_json')
        ingredientes = json.loads(ingredientes_json) if ingredientes_json else []
        sucursal = int(request.POST.get('sucursal'))
        
        if(sucursal == 1):
            fs.agregar_productos_vh(nombre,existencias,precio,categoria,ingredientes,estado,punto_reorden,sucursal)
        elif (sucursal == 2):
            fs.agregar_productos_moctezuma(nombre,existencias,precio,categoria,ingredientes,estado,punto_reorden,sucursal)
            
        elif (sucursal == 3):
            fs.agregar_productos_moctezuma(nombre,existencias,precio,categoria,ingredientes,estado,punto_reorden,2)
            fs.agregar_productos_vh(nombre,existencias,precio,categoria,ingredientes,estado,punto_reorden,1)
            
        return redirect('productos')
    
    context = {
        'prvh':productos_vh,
        'prmc':productos_mc,
        'cats':categorias,
        'template' : template    
    }

    return render(request,'productos.html',context)


@gerente_ventas_required
def editarProducto(request):
    if(request.method == 'POST'):
        idP = request.POST.get('idP')
        nombre = request.POST.get('nombre')
        existencias_str = request.POST.get('existencias')
        existencias = int(existencias_str) if existencias_str and existencias_str.isdigit() else None
        precio = int(request.POST.get('precio'))
        categoria = request.POST.get('categoria')
        estado = True if request.POST.get('estado') == 'on' else False
        punto_reorden = int(request.POST.get('punto_reorden'))
        #ingredientes_json = request.POST.get('ingredientes_json')
        #ingredientes = json.loads(ingredientes_json) if ingredientes_json else []

        sucursal = int(request.POST.get('sucursal'))

        if(sucursal == 1):
            fs.editar_producto_vh(idP,nombre,existencias,precio,categoria,estado,punto_reorden)
        elif (sucursal == 2):
            fs.editar_producto_mc(idP,nombre,existencias,precio,categoria,estado,punto_reorden)
            
        elif (sucursal == 3):
            fs.editar_producto_vh(idP,nombre,existencias,precio,categoria,estado,punto_reorden)
            fs.editar_producto_mc(idP,nombre,existencias,precio,categoria,estado,punto_reorden)
        return JsonResponse({'mensaje': 'Producto editado correctamente'}, status=200)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def eliminarProducto(request, sucursal_id, producto_id):
    if request.method == 'DELETE':
        sucursal = int(sucursal_id)
        producto = str(producto_id)
        try:
            fs.eliminarProducto(sucursal, producto)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)