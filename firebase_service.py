from firebase_admin import db
import firebase_config
# *** Funciones Vista Hermosa

#Funciones add 
def agregar_productos_vh(nombre,existencias,precio,categoria,ingredientes):
    ref = db.reference("/vistahermosa/productos")
    n_ref = ref.push()
    n_uid = n_ref.key


    nuevo_producto = {
        'id': n_uid,
        "nombre" : nombre,
        "existencias" : existencias,
        "precio" : precio,
        'categoria': categoria,
        'ingredientes':ingredientes,
    }
    n_ref.set(nuevo_producto)
    print("Producto(s) añadido correctamente")


def agregar_insumos_vh(nombre,cantidad,medida):
    ref = db.reference("/vistahermosa/insumos")
    nuevo_insumo = {
        'nombre':nombre,
        'cantidad':cantidad,
        'medida':medida
    }
    ref.push(nuevo_insumo)
    print('Insumo(s) agregado correctamente')

def registrar_pedido(folio, #
                     fecha_registro, #
                     nombre_cliente, #
                     telefono, #
                     productos,
                     especificaciones,
                     forma_entrega,
                     metodo_pago,
                     total,
                     gran_total,
                     fecha_entrega,
                     hora_entrega,
                     at_no_emp,
                     at_nom_emp,
                     estado,
                     restante_pagado,
                     anticipo=None,
                     recibe=None,
                     cel=None,
                     direccion=None,
                     referencias=None,
                     costo_envio=None,
                     recibido=None,
                     cambio=None,
                     num_operacion=None,
                     sucursal=None,
                     mix_ef=None,
                     mix_tar=None
                     ):
    pedido_data = {
        'folio':folio, #
        'fecha_registro':fecha_registro, #
        'nombre_cliente':nombre_cliente, # 
        'telefono':telefono, #
        
        'productos':productos,
        
        'especificaciones':especificaciones,
        
        'forma_entrega':forma_entrega,

        'sucursal' : sucursal,

        'recibe':recibe,
        'cel':cel,
        'direccion':direccion,
        'referencias':referencias,
        'costo_envio':costo_envio,

        'fecha_entrega':fecha_entrega,
        'hora_entrega':hora_entrega,

        'total':total,
        'gran_total':gran_total,
        'anticipo':anticipo,
        'restante_pagado' : restante_pagado,

        'metodo_pago':metodo_pago,

        'recibido': recibido,

        'cambio': cambio,

        'num_operacion': num_operacion,

        'mix_ef' : mix_ef,

        'mix_tar' : mix_tar,

        'at_no_emp' : at_no_emp,

        'at_nom_emp' : at_nom_emp,

        'estado': estado,
        
    }

    pedido_data = {i: j for i, j in pedido_data.items() if j is not None}

    ref = db.reference('/pedidos')
    nuevo_pedido=ref.push(pedido_data)
    return nuevo_pedido.key


def registrar_venta_vh(
    ubicacion,
    fecha_venta,
    no_venta,
    at_nom_emp,
    at_no_emp,
    productos,
    total,
    metodo_pago,
    recibido=None,
    cambio=None,
    no_operacion=None):

    venta_data = {
        'ubicacion':ubicacion,
        'fecha_venta':fecha_venta,
        'no_venta':no_venta,
        'at_nom_emp':at_nom_emp,
        'at_no_emp':at_no_emp,
        'productos':productos,
        'total':total,
        'metodo_pago':metodo_pago,
        'recibido':recibido,
        'cambio':cambio,
        'no_operacion':no_operacion
    }
    venta_data = {i: j for i, j in venta_data.items() if j is not None}
    ref = db.reference('/vistahermosa/ventas')
    ref.push(venta_data)
    return 'Venta registrada'

def agregar_codigos(codigo):
    ref = db.reference('/codigos')
    ref.push(codigo)
    print('listo')

#Funciones get
def obtener_productos_vh():
    ref = db.reference("/vistahermosa/productos").get()
    return (ref)

def obtener_insumos_vh():
    ref = db.reference("/vistahermosa/insumos/").get()
    print(ref)

def obtener_usuarios_vh():
    ref = db.reference('/usuarios/')
    query = ref.order_by_child('sucursal').equal_to('vista hermosa').get()
    if query:
        for uid, datos in query.items():
            print(f"{uid}: {datos}")
    else:
        print("No se encontraron usuarios con sucursal 'vista hermosa'")

def obtener_folio_vh():
    ref = db.reference('/folio/vistahermosa/folio').get()
    return (ref)

def ref_folio_vh():
    ref = db.reference('/folio/vistahermosa/folio')
    return (ref)

def obtener_pedidos():
    ref = db.reference('/pedidos').get()
    return (ref)

def obtener_seriabilidad_vh():
    ref = db.reference('/seriabilidad/vistahermosa/venta').get()
    return (ref)


def ref_seriabilidad_vh():
    ref = db.reference('/seriabilidad/vistahermosa/venta')
    return (ref)

# *** Funciones moctezuma

#Funciones add
def agregar_productos_moctezuma(nombre,existencias,precio,categoria,ingredientes):
    ref = db.reference("/moctezuma/productos")
    n_ref = ref.push()
    n_uid = n_ref.key


    nuevo_producto = {
        'id' : n_uid,
        "nombre" : nombre,
        "existencias" : existencias,
        "precio" : precio,
        'categoria': categoria,
        'ingredientes':ingredientes,
    }
    n_ref.set(nuevo_producto)
    print("Producto(s) añadido correctamente")


def registrar_venta_mc(
    ubicacion,
    fecha_venta,
    no_venta,
    at_nom_emp,
    at_no_emp,
    productos,
    total,
    metodo_pago,
    recibido=None,
    cambio=None,
    no_operacion=None):

    venta_data = {
        'ubicacion':ubicacion,
        'fecha_venta':fecha_venta,
        'no_venta':no_venta,
        'at_nom_emp':at_nom_emp,
        'at_no_emp':at_no_emp,
        'productos':productos,
        'total':total,
        'metodo_pago':metodo_pago,
        'recibido':recibido,
        'cambio':cambio,
        'no_operacion':no_operacion
    }
    venta_data = {i: j for i, j in venta_data.items() if j is not None}
    ref = db.reference('/moctezuma/ventas')
    ref.push(venta_data)
    return 'Venta registrada'



#Funciones get
def obtener_productos_moctezuma():
    ref = db.reference("/moctezuma/productos").get()
    return (ref)

def obtener_folio_mc():
    ref = db.reference('/folio/moctezuma/folio').get()
    return (ref)
#categorias

def add_cat(categoria):
    ref = db.reference('/categorias')
    nueva_cat = {
        'nombre':categoria
    }
    ref.push(nueva_cat)

def ref_folio_mc():
    ref = db.reference('/folio/moctezuma/folio')
    return (ref)


def obtener_seriabilidad_mc():
    ref = db.reference('/seriabilidad/moctezuma/venta').get()
    return (ref)

def ref_seriabilidad_mc():
    ref = db.reference('/seriabilidad/moctezuma/venta')
    return (ref)


#ACTUALIZACION DE ATRIBUTOS

def act_pedido_estado(folio):
    print('1')
    ref = db.reference('/pedidos/')
    
    pedidos = ref.order_by_child('folio').equal_to(folio).get()

    for key, pedido in pedidos.items():  # Itera sobre los pedidos encontrados
        db.reference(f'/pedidos/{key}').update({'estado': 1})  # Actualiza cada pedido encontrado

    return 'Estado actualizado'
