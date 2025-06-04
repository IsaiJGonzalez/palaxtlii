from django.shortcuts import render, redirect
from firebase_config import fr_db
import firebase_service as fs
import json

# Create your views here.
def productos(request):
    productos_vh = list(fs.obtener_productos_vh().values()) if fs.obtener_productos_vh() else []
    productos_mc = list(fs.obtener_productos_moctezuma().values()) if fs.obtener_productos_moctezuma() else []
    categorias_r = fr_db.child('categorias').get()
    categorias = [{"id": k, "nombre": v["nombre"]} for k, v in categorias_r.items()]

    if (request.method == 'POST'):
            #atributos
        nombre = request.POST.get('nombre')
        existencias_str = request.POST.get('existencias')
        existencias = int(existencias_str) if existencias_str and existencias_str.isdigit() else None
        precio = int(request.POST.get('precio'))
        categoria = request.POST.get('categoria')
        ingredientes_json = request.POST.get('ingredientes_json')
        print('ingredientes json ', ingredientes_json)
        ingredientes = json.loads(ingredientes_json) if ingredientes_json else []
        print('ingredientes ',ingredientes)
        sucursal = int(request.POST.get('sucursal'))
        
        if(sucursal == 1):
            fs.agregar_productos_vh(nombre,existencias,precio,categoria,ingredientes)

        elif (sucursal == 2):
            fs.agregar_productos_moctezuma(nombre,existencias,precio,categoria,ingredientes)
            
        elif (sucursal == 3):
            fs.agregar_productos_moctezuma(nombre,existencias,precio,categoria,ingredientes)
            fs.agregar_productos_vh(nombre,existencias,precio,categoria,ingredientes)
            
        return redirect('productos')
    return render(request,'productos.html',{'prvh':productos_vh,'prmc':productos_mc,'cats':categorias})