from firebase_admin import db
import firebase_config
from datetime import date



#*** FUNCIONES GLOBALES

from firebase_admin import db
from datetime import datetime, date


# ==============================
# Helpers
# ==============================

def to_float(v):
    try:
        return float(v)
    except:
        return 0.0


# ==============================
# 1️⃣ Obtener pedidos activos (solo folio)
# ==============================

def obtener_folios_activos():
    ref = db.reference("pedidos")

    pedidos = ref.order_by_child("estado").equal_to(0).get()

    resultado = []

    if pedidos:
        for pid, p in pedidos.items():
            resultado.append({
                "id": pid,
                "folio": p.get("folio")
            })

    return resultado


# ==============================
# 2️⃣ Obtener pedido completo por ID
# ==============================

def obtener_pedido_por_id(pedido_id):
    ref = db.reference(f"pedidos/{pedido_id}")
    return ref.get()


# ==============================
# EDITAR PEDIDO (VERSIÓN CORREGIDA)
# ==============================
def editar_pedido(pedido_id, data, nombre_emp):

    ref = db.reference("pedidos").child(pedido_id)
    pedido = ref.get()

    if not pedido:
        return {"ok": False, "error": "Pedido no existe"}

    # =============================
    # NO EDITAR ENTREGADOS
    # =============================
    if pedido.get("estado") == 1:
        return {"ok": False, "error": "Pedido ya entregado"}

    # =============================
    # VALIDACIONES
    # =============================

    telefono = data.get("telefono", "").strip()
    if not telefono:
        return {"ok": False, "error": "Teléfono obligatorio"}

    fecha_entrega = data.get("fecha_entrega")
    if fecha_entrega:
        f = datetime.strptime(fecha_entrega, "%Y-%m-%d").date()
        if f < date.today():
            return {"ok": False, "error": "Fecha inválida"}
    else:
        fecha_entrega = pedido.get("fecha_entrega")

    forma_entrega = data.get("forma_entrega", "tienda")

    # =============================
    # COSTO ENVÍO
    # =============================

    costo_envio_nuevo = int(data.get("costo_envio") or 0)

    # Si es tienda → envío en 0 SIEMPRE
    if forma_entrega == "tienda":
        costo_envio_nuevo = 0

    # =============================
    # PRODUCTOS
    # =============================

    productos_front = data.get("productos", [])

    if not productos_front:
        return {"ok": False, "error": "Debe haber al menos 1 producto"}

    productos_bd = pedido.get("productos", {})

    # convertir lista a dict
    if isinstance(productos_bd, list):
        productos_bd = {str(i): p for i, p in enumerate(productos_bd)}

    max_index = -1
    if productos_bd:
        max_index = max(int(i) for i in productos_bd.keys())

    suma_productos = 0

    for prod in productos_front:

        cantidad = int(prod.get("cantidad", 0))
        precio = int(prod.get("precio_unitario", 0))

        if cantidad <= 0 or precio <= 0:
            return {"ok": False, "error": "Cantidad/precio inválidos"}

        importe = cantidad * precio
        suma_productos += importe

        idx = prod.get("index")

        prod_obj = {
            "cantidad": cantidad,
            "descripcion": prod.get("descripcion", ""),
            "precio_unitario": precio,
            "importe": importe
        }

        # editar existente
        if idx is not None and str(idx) in productos_bd:
            productos_bd[str(idx)] = prod_obj
        else:
            # nuevo producto
            max_index += 1
            productos_bd[str(max_index)] = prod_obj

    # =============================
    # RECALCULAR TOTALES DESDE CERO
    # =============================

    total_final = suma_productos + costo_envio_nuevo

    anticipo = int(float(pedido.get("anticipo") or 0))

    gran_total_final = total_final - anticipo
    if gran_total_final < 0:
        gran_total_final = 0

    # =============================
    # UPDATE
    # =============================

    update_data = {
        "telefono": telefono,
        "cel": data.get("cel", ""),
        "direccion": data.get("direccion", ""),
        "referencias": data.get("referencias", ""),
        "forma_entrega": forma_entrega,
        "costo_envio": costo_envio_nuevo,
        "sucursal": data.get("sucursal", "") if forma_entrega == "tienda" else "",
        "fecha_entrega": fecha_entrega,
        "hora_entrega": data.get("hora_entrega", ""),
        "especificaciones": data.get("especificaciones", ""),
        "productos": productos_bd,
        "total": total_final,
        "gran_total": gran_total_final,
        "editado_por": nombre_emp,
        "fecha_edicion": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    ref.update(update_data)

    return {"ok": True}


# *** Funciones Vista Hermosa

#Funciones add 
def agregar_productos_vh(nombre,existencias,precio,categoria,ingredientes,estado,punto_reorden,sucursal):
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
        'estado':estado,
        'punto_reorden':punto_reorden,
        'sucursal':sucursal
    }
    n_ref.set(nuevo_producto)
    print("Producto(s) añadido correctamente")

def eliminarProducto(sucursal,id):
    suc = 'vistahermosa' if sucursal == 1 else 'moctezuma' if sucursal == 2 else ''
    print(suc)
    ref = db.reference(f'{suc}/productos/{id}')
    ref.delete()
    print('PR elimiado')

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
    no_operacion=None,
    mix_ef = None,
    mix_tar = None,
    descuento_aplicado = 0, # Dinero descontado
    info_descuento = "Ninguno" # Texto (ej: "10% Manual", "Tarjeta CUPON1")
    ):

    venta_data = {
        'ubicacion':ubicacion,
        'fecha_venta':fecha_venta,
        'no_venta':no_venta,
        'at_nom_emp':at_nom_emp,
        'at_no_emp':at_no_emp,
        'productos':productos,
        'total':total, #total con descuento
        'metodo_pago':metodo_pago,
        'recibido':recibido,
        'cambio':cambio,
        'no_operacion':no_operacion,
        'mix_ef':mix_ef,
        'mix_tar':mix_tar,
        # GUARDAMOS INFO DEL DESCUENTO
        'descuento_monto': descuento_aplicado,
        'descuento_detalle': info_descuento
    }
    venta_data = {i: j for i, j in venta_data.items() if j is not None}
    fecha_str = fecha_venta if isinstance(fecha_venta, str) else fecha_venta.strftime('%Y-%m-%d')
    ref = db.reference(f'/vistahermosa/ventas/{fecha_str}')
    ref.push(venta_data)
    return 'Venta registrada'

def agregar_codigos(codigo):
    ref = db.reference('/codigos/')
    codigo_nuevo = {
        'codigo' : codigo
    }
    ref.push(codigo_nuevo)
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


def obtener_producto_vh(id):
    doc_ref = db.reference(f'/vistahermosa/productos/{id}')
    producto = doc_ref.get()
    nombre = producto.get('nombre')
    return nombre


def ref_seriabilidad_vh():
    ref = db.reference('/seriabilidad/vistahermosa/venta')
    return (ref)


def restar_producto_vh(id,cantidad):
    try:
        ref = db.reference(f'vistahermosa/productos/{id}')
        existencias = db.reference(f'vistahermosa/productos/{id}/existencias').get()
        ex_act = existencias - cantidad
        ref.update({'existencias':ex_act})
    except Exception as e:
        print('Error: ',e)


def editar_producto_vh(id,nombre,existencias,precio,categoria,estado,punto_reorden):
    try:
        ref = db.reference(f'vistahermosa/productos/{id}')
        ref.update({
            'categoria':categoria,
            'estado':estado,
            'existencias':existencias,
            'nombre' : nombre,
            'precio' : precio,
            'punto_reorden' : punto_reorden,
            
        })
        print('Producto editado correctamente')
    except Exception as e:
        print('Error al editar p: ',e)

# *** Funciones moctezuma

#Funciones add
def agregar_productos_moctezuma(nombre,existencias,precio,categoria,ingredientes,estado,punto_reorden,sucursal):
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
        'estado':estado,
        'punto_reorden':punto_reorden,
        'sucursal':sucursal
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
    no_operacion=None,
    mix_ef = None,
    mix_tar = None,
    descuento_aplicado = 0, # Dinero descontado
    info_descuento = "Ninguno" # Texto (ej: "10% Manual", "Tarjeta CUPON1")
    ):

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
        'no_operacion':no_operacion,
        'mix_ef':mix_ef,
        'mix_tar':mix_tar,
        # GUARDAMOS INFO DEL DESCUENTO
        'descuento_monto': descuento_aplicado,
        'descuento_detalle': info_descuento
    }
    venta_data = {i: j for i, j in venta_data.items() if j is not None}
    fecha_str = fecha_venta if isinstance(fecha_venta, str) else fecha_venta.strftime('%Y-%m-%d')

    ref = db.reference(f'/moctezuma/ventas/{fecha_str}')
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


def obtener_producto_mc(id):
    doc_ref = db.reference(f'/moctezuma/productos/{id}')
    producto = doc_ref.get()
    nombre = producto.get('nombre')
    return nombre


def ref_seriabilidad_mc():
    ref = db.reference('/seriabilidad/moctezuma/venta')
    return (ref)

def restar_producto_mc(id,cantidad):
    try:
        ref = db.reference(f'moctezuma/productos/{id}')
        existencias = db.reference(f'moctezuma/productos/{id}/existencias').get()
        ex_act = existencias - cantidad
        ref.update({'existencias':ex_act})
    except Exception as e:
        print('Error: ',e)


#ACTUALIZACION DE ATRIBUTOS

def act_pedido_estado(folio):

    ref = db.reference('/pedidos/')
    
    pedidos = ref.order_by_child('folio').equal_to(folio).get()

    for key, pedido in pedidos.items():  # Itera sobre los pedidos encontrados
        db.reference(f'/pedidos/{key}').update({'estado': 1})  # Actualiza cada pedido encontrado

    return 'Estado actualizado'


def editar_producto_mc(id,nombre,existencias,precio,categoria,estado,punto_reorden):
    try:
        ref = db.reference(f'moctezuma/productos/{id}')
        ref.update({
            'categoria':categoria,
            'estado':estado,
            'existencias':existencias,
            'nombre' : nombre,
            'precio' : precio,
            'punto_reorden' : punto_reorden,
            
        })
        print('Producto editado correctamente')
    except Exception as e:
        print('Error al editar p: ',e)


def obtener_categorias():
    try:

        ref = db.reference('categorias/').get()
        return(ref)
    except Exception as e:
        print('Error al obtener Categoriass: ', e)


def obtener_codigos():
    try:
        ref = db.reference('codigos/').get()
        return (ref)
    except Exception as e:
        print('Error al obtener codigos: ', e)



#CAJASSSSSSS

def apertura_caja_vh(
    no_emp, fecha_asignacion, b1000, b500, b200, b100, b50, b20, monedas, fondo_caja, estado
):
    try:
        ref = db.reference('vistahermosa/apertura_caja')
        n_ref = ref.push()
        n_uid = n_ref.key

        #ruta del empleado
        e_ref = db.reference(f'empleados/{no_emp}')

        apertura_caja = {
            'id':n_uid,
            'no_emp':no_emp,
            'fecha_asignacion' : fecha_asignacion,
            '1000' : b1000,
            '500' : b500,
            '200' : b200,
            '100' : b100,
            '50' : b50,
            '20' : b20,
            'monedas' : monedas,
            'fondo_caja':fondo_caja,
            'estado' : estado
        }
        n_ref.set(apertura_caja)

        #añadir la id de la caja activa
        e_ref.update({'id_caja':n_uid})
        print('Caja abierta correctamente')
    except Exception as e:
        print('Error al abrir caja: ', e)



def apertura_caja_mc(
    no_emp, fecha_asignacion, b1000, b500, b200, b100, b50, b20, monedas, fondo_caja, estado
):
    try:
        ref = db.reference('moctezuma/apertura_caja')
        n_ref = ref.push()
        n_uid = n_ref.key

        #ruta del empleado
        e_ref = db.reference(f'empleados/{no_emp}')

        apertura_caja = {
            'id':n_uid,
            'no_emp':no_emp,
            'fecha_asignacion' : fecha_asignacion,
            '1000' : b1000,
            '500' : b500,
            '200' : b200,
            '100' : b100,
            '50' : b50,
            '20' : b20,
            'monedas' : monedas,
            'fondo_caja':fondo_caja,
            'estado' : estado
        }
        n_ref.set(apertura_caja)
        
        #añadir la id de la caja activa
        e_ref.update({'id_caja':n_uid})

        print('Caja abierta correctamente')
    except Exception as e:
        print('Error al abrir caja: ', e)






def activar_caja_emp(id):
    ref = db.reference(f'empleados/{id}')
    ref.update({'caja_activa':True})

def consultar_caja_activa(id):
    ref = db.reference(f'empleados/{id}').get()
    return ref.get('caja_activa')

def consultar_id_caja_emp(id):
    ref = db.reference(f'empleados/{id}').get()
    return ref.get('id_caja')

def consultar_monto_apertura(id, suc):
    id_caja = consultar_id_caja_emp(id)
    sucursal = 'vistahermosa' if suc == 1 else 'moctezuma'
    data = db.reference(f'{sucursal}/apertura_caja/{id_caja}').get()
    
    # Si data es una tupla (dict, key)
    if isinstance(data, tuple):
        data = data[0]
    
    return data.get('fondo_caja') if data else None

def consultar_id_corte_caja_emp(id):
    ref = db.reference(f'empleados/{id}').get()
    return ref.get('id_corte')

def desactivar_caja_emp(id):
    ref = db.reference(f'empleados/{id}')
    ref.update({'caja_activa':False})

def limpiar_cajas_empleado(id):
    ref = db.reference(f'empleados/{id}')
    ref.update({
        'id_caja':'',
        'id_corte' : ''
    })


def desactivar_apertura_caja(id,sucursal):
    if sucursal == 1:
        ref = db.reference(f'vistahermosa/apertura_caja/{id}')
        ref.update({'estado' : False})
    elif sucursal == 2:
        ref = db.reference(f'moctezuma/apertura_caja/{id}')
        ref.update({'estado' : False})

def consultar_monto_en_caja(id_corte,sucursal):
    if sucursal == 1 :
        ref = db.reference(f'vistahermosa/corte_caja/{id_corte}/esperado_en_caja').get()
        return ref
    elif sucursal == 2: 
        ref = db.reference(f'moctezuma/corte_caja/{id_corte}/esperado_en_caja').get()
        return ref

def consultar_restante_pedido(folio):
    ref = db.reference('pedidos/')
    pedidos = ref.order_by_child('folio').equal_to(folio).get()

    for key, pedido in pedidos.items():
        return pedido.get('gran_total')
    return None

def consultar_confirmacion(codigo):
    codigos = db.reference('codigos/').get()
    for _, valor in codigos.items():
        if valor.get('codigo') == codigo:
            return True
    return False

def consultar_sucursal(sucursal):
    ruta = 'vistahermosa' if sucursal == 1 else 'moctezuma' if sucursal == 2 else None
    ref = db.reference(f'{ruta}/locacion').get()
    return ref

def consultar_corte(suc,corte_id):
    sucursal = 'vistahermosa' if suc == 1 else 'moctezuma' if suc == 2 else None
    ref = db.reference(f'{sucursal}/corte_caja/{corte_id}').get()
    return ref

def consultar_ventas_vh():
    #obteniendo la id
    hoy = date.today()
    #print(hoy)
    fecha = hoy.strftime(f"%Y-%m-{hoy.day}")
    #print(fecha)

    ref = db.reference(f'vistahermosa/ventas/{hoy}')
    ventas = ref.get()
    if not ventas:
        return []


    return list(ventas.values())



def consultar_ventas_mc():
    hoy = date.today()
    fecha = hoy.strftime(f"%Y-%m-{hoy.day}")
    #fecha = '2025-06-22'
    ref = db.reference(f'moctezuma/ventas/{hoy}')
    ventas = ref.get()
    if not ventas:
        return []

    return list(ventas.values())


def verificar_exis_empleado(no_emp):
    ref = db.reference(f'empleados/{no_emp}').get()
    return ref is not None

def cambiar_locacion_empleado(no_emp, locacion):
    ref = db.reference(f'empleados/{no_emp}')
    ref.update({'sucursal':locacion})

def cambiar_contrasena(no_emp,new_psw):
    try:
        ref = db.reference(f'empleados/{no_emp}')
        ref.update({'contrasena' : new_psw})
    except Exception as e:
        print('Error al cambiar contraseña: ',e)

def registrar_retiro(sucursal, data):
    nuevo_retiro = {
        'apertura_id': data.get('apertura_id'),
        'corte_id': data.get('corte_id'),
        'numero_empleado': data.get('numero_empleado'),
        'retira': data.get('retira'),
        'fecha': data.get('fecha'),
        'monto': data.get('monto'),
        'motivo': data.get('motivo')
    }

    id_corte = data.get('corte_id')
    monto = data.get('monto')

    if sucursal == 1:
        ref = db.reference('vistahermosa/retiros')
        ref_corte = db.reference(f'vistahermosa/corte_caja/{id_corte}')
        datos_corte = ref_corte.get()
        #valores esperados en corte
        valor_esperado_act = datos_corte.get('esperado_en_caja')
        nuevo_valor_esperado = valor_esperado_act - monto
        ref_corte.update({'esperado_en_caja': nuevo_valor_esperado})
        
        #valores de retiros en corte
        valor_retiro_act = datos_corte.get('retiros')
        nuevo_valor_retiro = valor_retiro_act + monto
        ref_corte.update({'retiros' : nuevo_valor_retiro})

    elif sucursal == 2:
        ref = db.reference('moctezuma/retiros')
        ref_corte = db.reference(f'moctezuma/corte_caja/{id_corte}')
        datos_corte = ref_corte.get()
        #valores esperados en corte
        valor_esperado_act = datos_corte.get('esperado_en_caja')
        nuevo_valor_esperado = valor_esperado_act - monto
        ref_corte.update({'esperado_en_caja': nuevo_valor_esperado})

        #valores de retiros en corte
        valor_retiro_act = datos_corte.get('retiros')
        nuevo_valor_retiro = valor_retiro_act + monto
        ref_corte.update({'retiros' : nuevo_valor_retiro})
        
    else:
        return
    ref.push(nuevo_retiro)


#FUNCIONES QUE ABREN EL CORTE DE CAJA PARA EL EMPLEADO
def corte_caja_vh(no_emp, apertura_id, fondo):
    try:
        ref = db.reference('vistahermosa/corte_caja')
        n_ref = ref.push()
        corte_id = n_ref.key

        # Ruta del empleado
        e_ref = db.reference(f'empleados/{no_emp}')

        corte_caja = {
            'id': corte_id,
            'apertura_id': apertura_id,
            'no_emp': no_emp,
            'fecha_corte': None,  # Se llenará cuando se cierre
            'estado': True,

            'ventas': {
                'efectivo': 0.0,
                'tarjeta': 0.0,
                'transferencia': 0.0
            },

            'pedidos' : {
                'efectivo': 0.0,
                'tarjeta': 0.0,
                'transferencia': 0.0
            },

            'retiros': 0.0,
            'monedas': 0.0,
            'billetes': {},
            'total_en_caja': 0.0,
            'esperado_en_caja': fondo,
            'diferencia': 0.0,
        }

        n_ref.set(corte_caja)

        # Actualizar referencia en el empleado
        e_ref.update({'id_corte': corte_id})

        print('Corte de caja inicial creado correctamente.')
    except Exception as e:
        print('Error al crear corte de caja: ', e)


def corte_caja_mc(no_emp, apertura_id,fondo):
    try:
        ref = db.reference('moctezuma/corte_caja')
        n_ref = ref.push()
        corte_id = n_ref.key

        # Ruta del empleado
        e_ref = db.reference(f'empleados/{no_emp}')

        corte_caja = {
            'id': corte_id,
            'apertura_id': apertura_id,
            'no_emp': no_emp,
            'fecha_corte': None,  # Se llenará cuando se cierre
            'estado': True,

            'ventas': {
                'efectivo': 0.0,
                'tarjeta': 0.0,
                'transferencia': 0.0
            },

            'pedidos' : {
                'efectivo': 0.0,
                'tarjeta': 0.0,
                'transferencia': 0.0
            },

            'retiros': 0.0,
            'monedas': 0.0,
            'billetes': {},
            'total_en_caja': 0.0,
            'esperado_en_caja': fondo,
            'diferencia': 0.0,
        }

        n_ref.set(corte_caja)

        # Actualizar referencia en el empleado
        e_ref.update({'id_corte': corte_id})

        print('Corte de caja inicial creado correctamente.')
    except Exception as e:
        print('Error al crear corte de caja: ', e)


#función para registrar ventas y pedidos en corte 
def registrar_en_corte_mc(corte_id,tipo,metodo_pago,ingreso,resumen=None):
    ref = db.reference(f'moctezuma/corte_caja/{corte_id}')
    if (tipo == 'pedido'):
        #validando si el metodo de pago es mixto
        if metodo_pago == "mixto":
            #1. si el metodo de pago es mixto se obtienen los valores de ingreso
            #almacenados en el diccionario
            tarjeta = float(ingreso.get("t")) #t = tarjeta
            efectivo = float(ingreso.get("e")) # e = efectivo
            #2. se ingresan los montos en el respectivo apartado para efectivo
            #y tarjeta 
            #Tarjeta: 
            path = f'pedidos/tarjeta'
            val_actual = ref.child(path).get()
            suma = val_actual + tarjeta if val_actual else tarjeta
            ref.child(path).set(suma)

            #Efectivo: 
            path = f'pedidos/efectivo'
            val_actual = ref.child(path).get()
            suma = val_actual + efectivo if val_actual else efectivo
            ref.child(path).set(suma)

            #Actualizando el esperado en caja
            val_e_act = ref.child('esperado_en_caja').get()
            suma_e = val_e_act + efectivo if val_e_act else efectivo
            ref.child('esperado_en_caja').set(suma_e)
        else:
            path = f'pedidos/{metodo_pago}'
            val_actual = ref.child(path).get()
            suma = val_actual + ingreso if val_actual else ingreso
            ref.child(path).set(suma)
            if (metodo_pago == 'efectivo'):
                val_e_act = ref.child('esperado_en_caja').get()
                suma_e = val_e_act + ingreso if val_e_act else ingreso
                ref.child('esperado_en_caja').set(suma_e)
            print('Ingreso del pedido registrado')
    elif (tipo == 'venta'):
        if metodo_pago == "mixto":
            #1. Obtenemos del ingreso lo pagado con efectivo y tarjeta
            efectivo = float(ingreso.get('e'))
            tarjeta = float(ingreso.get('t'))
            #2. se ingresan los montos en el respectivo apartado para efectivo
            #y tarjeta 
            #Tarjeta: 
            path = f'ventas/tarjeta'
            val_actual = ref.child(path).get()
            suma = val_actual + tarjeta if val_actual else tarjeta
            ref.child(path).set(suma)

            #Efectivo: 
            path = f'ventas/efectivo'
            val_actual = ref.child(path).get()
            suma = val_actual + efectivo if val_actual else efectivo
            ref.child(path).set(suma)

            #Actualizando el esperado en caja
            val_e_act = ref.child('esperado_en_caja').get()
            suma_e = val_e_act + efectivo if val_e_act else efectivo
            ref.child('esperado_en_caja').set(suma_e)
        else:
            path = f'ventas/{metodo_pago}'
            val_actual = ref.child(path).get()
            suma = val_actual + ingreso if val_actual else ingreso
            ref.child(path).set(suma)
            if (metodo_pago == 'efectivo'):
                val_e_act = ref.child('esperado_en_caja').get()
                suma_e = val_e_act + ingreso if val_e_act else ingreso
                ref.child('esperado_en_caja').set(suma_e)
            print('Ingreso de la venta registrada')

        # Extraemos el descuento del resumen (si existe)
        descuento_monto = float(resumen.get('descuento_monto', 0))
        
        if descuento_monto > 0:
            # 1. Acumular el monto total descontado en el día
            path_desc_monto = 'ventas/total_descontado_dinero'
            val_desc_monto = ref.child(path_desc_monto).get() or 0
            ref.child(path_desc_monto).set(val_desc_monto + descuento_monto)

            # 2. Contar cuántos descuentos se hicieron
            path_desc_count = 'ventas/cantidad_descuentos_aplicados'
            val_desc_count = ref.child(path_desc_count).get() or 0
            ref.child(path_desc_count).set(val_desc_count + 1)

        print('Ingreso de la venta y descuento registrado')

        #ingresando la venta al corte
        venta_historica = ref.child('venta_historica')
        #verificamos las ventas que hay
        ventas_actuales = venta_historica.get() or {}
        # Calcular el siguiente número
        siguiente_num = str(len(ventas_actuales) + 1)
        # Guardar la nueva venta en esa posición
        venta_historica.child(siguiente_num).set(resumen)

    return

def registrar_en_corte_vh(corte_id,tipo,metodo_pago,ingreso,resumen=None):
    ref = db.reference(f'vistahermosa/corte_caja/{corte_id}')
    if (tipo == 'pedido'):
        #validando si el metodo de pago es mixto
        if metodo_pago == "mixto":
            #1. si el metodo de pago es mixto se obtienen los valores de ingreso
            #almacenados en el diccionario
            tarjeta = float(ingreso.get("t")) #t = tarjeta
            efectivo = float(ingreso.get("e")) # e = efectivo
            #2. se ingresan los montos en el respectivo apartado para efectivo
            #y tarjeta 
            #Tarjeta: 
            path = f'pedidos/tarjeta'
            val_actual = ref.child(path).get()
            suma = val_actual + tarjeta if val_actual else tarjeta
            ref.child(path).set(suma)

            #Efectivo: 
            path = f'pedidos/efectivo'
            val_actual = ref.child(path).get()
            suma = val_actual + efectivo if val_actual else efectivo
            ref.child(path).set(suma)

            #Actualizando el esperado en caja
            val_e_act = ref.child('esperado_en_caja').get()
            suma_e = val_e_act + efectivo if val_e_act else efectivo
            ref.child('esperado_en_caja').set(suma_e)
        else:
            path = f'pedidos/{metodo_pago}'
            val_actual = ref.child(path).get()
            suma = val_actual + ingreso if val_actual else ingreso
            ref.child(path).set(suma)
            if (metodo_pago == 'efectivo'):
                val_e_act = ref.child('esperado_en_caja').get()
                suma_e = val_e_act + ingreso if val_e_act else ingreso
                ref.child('esperado_en_caja').set(suma_e)
            print('Ingreso del pedido registrado')
    elif (tipo == 'venta'):
        if metodo_pago == "mixto":
            #1. Obtenemos del ingreso lo pagado con efectivo y tarjeta
            efectivo = float(ingreso.get('e'))
            tarjeta = float(ingreso.get('t'))
            #2. se ingresan los montos en el respectivo apartado para efectivo
            #y tarjeta 
            #Tarjeta: 
            path = f'ventas/tarjeta'
            val_actual = ref.child(path).get()
            suma = val_actual + tarjeta if val_actual else tarjeta
            ref.child(path).set(suma)

            #Efectivo: 
            path = f'ventas/efectivo'
            val_actual = ref.child(path).get()
            suma = val_actual + efectivo if val_actual else efectivo
            ref.child(path).set(suma)

            #Actualizando el esperado en caja
            val_e_act = ref.child('esperado_en_caja').get()
            suma_e = val_e_act + efectivo if val_e_act else efectivo
            ref.child('esperado_en_caja').set(suma_e)
        else:
            path = f'ventas/{metodo_pago}'
            val_actual = ref.child(path).get()
            suma = val_actual + ingreso if val_actual else ingreso
            ref.child(path).set(suma)
            if (metodo_pago == 'efectivo'):
                val_e_act = ref.child('esperado_en_caja').get()
                suma_e = val_e_act + ingreso if val_e_act else ingreso
                ref.child('esperado_en_caja').set(suma_e)
            print('Ingreso de la venta registrada')
        
        # Extraemos el descuento del resumen (si existe)
        descuento_monto = float(resumen.get('descuento_monto', 0))
        
        if descuento_monto > 0:
            # 1. Acumular el monto total descontado en el día
            path_desc_monto = 'ventas/total_descontado_dinero'
            val_desc_monto = ref.child(path_desc_monto).get() or 0
            ref.child(path_desc_monto).set(val_desc_monto + descuento_monto)

            # 2. Contar cuántos descuentos se hicieron
            path_desc_count = 'ventas/cantidad_descuentos_aplicados'
            val_desc_count = ref.child(path_desc_count).get() or 0
            ref.child(path_desc_count).set(val_desc_count + 1)

        print('Ingreso de la venta y descuento registrado')


        #ingresando la venta al corte
        venta_historica = ref.child('venta_historica')
        #verificamos las ventas que hay
        ventas_actuales = venta_historica.get() or {}
        # Calcular el siguiente número
        siguiente_num = str(len(ventas_actuales) + 1)
        # Guardar la nueva venta en esa posición
        venta_historica.child(siguiente_num).set(resumen)

    return

def obtener_tarjetas_descuento():
    """
    Consulta todas las tarjetas disponibles en la raíz.
    Retorna un diccionario: {'san_valentin': {...}, 'otro_codigo': {...}}
    """
    ref = db.reference('tarjetas_descuento')
    return ref.get() or {}

def crear_tarjeta_descuento(codigo, descuento, tipo, existencias,activo=True):
    """
    Crea o sobrescribe una tarjeta de descuento.
    codigo: str (Ej: 'san_valentin')
    descuento: float/int (Ej: 15)
    tipo: str (Ej: '%' o '$')
    existencias: int (Ej: 100)
    """
    ref = db.reference(f'tarjetas_descuento/{codigo}')
    data = {
        'referencia' : int(codigo),
        'descuento': descuento,
        'tipo': tipo,
        'existencias': existencias,
        'activo': activo
    }
    ref.set(data)
    return True

def restar_uso_tarjeta(codigo):
    """
    Resta 1 a las existencias de la tarjeta usada.
    Si llega a 0, podrías optar por desactivarla (opcional).
    """
    ref = db.reference(f'tarjetas_descuento/{codigo}')
    tarjeta = ref.get()
    
    if tarjeta and tarjeta.get('existencias', 0) > 0:
        nuevas_existencias = tarjeta['existencias'] - 1
        ref.update({'existencias': nuevas_existencias})
        
        # Opcional: Desactivar si llega a 0
        if nuevas_existencias <= 0:
            ref.update({'activo': False})

###REGISTRAR ABONOS

def registrar_abono(id_abono, folio, fecha, abono, metodo_pago, sucursal, gran_total_restante):
    try:
        # 1. Guardar el abono en abonos/{id_abono}/{siguiente_id}
        abonos_ref = db.reference(f"abonos/{id_abono}")
        abonos_existentes = abonos_ref.get()
        siguiente_id = len(abonos_existentes) + 1 if abonos_existentes else 1

        nuevo_abono = {
            "monto": abono,
            "fecha": fecha,
            "metodo": metodo_pago,
            "folio_nota": folio,
            "sucursal": sucursal
        }

        abonos_ref.child(str(siguiente_id)).set(nuevo_abono)

        # 2. Buscar el pedido que tenga el folio == id_abono
        pedidos_ref = db.reference("pedidos")
        pedidos_query = pedidos_ref.order_by_child("folio").equal_to(id_abono)
        resultados = pedidos_query.get()

        if not resultados:
            print(f"❌ No se encontró ningún pedido con folio {id_abono}")
            return

        # 3. Obtener UID del pedido encontrado
        for uid_pedido, datos in resultados.items():
            anticipo_actual = float(datos.get("anticipo", 0))
            nuevo_anticipo = anticipo_actual + float(abono)

            gran_total_actual = float(datos.get("gran_total", 0))
            nuevo_gran_total = gran_total_actual - float(abono)

            # 4. Armar datos a actualizar
            datos_actualizados = {
                "anticipo": str(nuevo_anticipo),
                "gran_total": nuevo_gran_total
            }

            # Verificar si el restante ya es cero
            if float(gran_total_restante) == 0.00:
                datos_actualizados["restante_pagado"] = True

            # Actualizar pedido
            pedidos_ref.child(uid_pedido).update(datos_actualizados)

            print(f"✅ Abono registrado correctamente.")
            print(f"Nuevo anticipo para pedido con UID {uid_pedido}: ${nuevo_anticipo:.2f}")
            return  # Salir después de actualizar uno

    except Exception as e:
        print(f"❌ Error al registrar abono: {e}")


##CERRAR CAJAS

def cerrar_cajas(sucursal,no_emp,apertura_id,corte_id,fecha_corte,billetes,monedas,total_en_caja):
    ruta = 'vistahermosa' if sucursal == 1 else 'moctezuma' if sucursal == 2 else None
    if ruta:
        ref_corte = db.reference(f'{ruta}/corte_caja/{corte_id}')
        esperado_en_caja = consultar_monto_en_caja(corte_id, sucursal)
        diferencia = esperado_en_caja - total_en_caja

        ref_corte.update({
            'diferencia': diferencia,
            'estado': False,
            'fecha_corte': fecha_corte,
            'billetes': billetes,
            'monedas': monedas,
            'total_en_caja': total_en_caja
        })
        desactivar_apertura_caja(apertura_id, sucursal)
        desactivar_caja_emp(no_emp)
        limpiar_cajas_empleado(no_emp)
    else:
        print('Error al cerrar cajas')



#CONSULTA DE CAJAS

def consultar_aperturas(sucursal):
    ruta = 'vistahermosa' if sucursal == 1 else 'moctezuma' if sucursal == 2 else None
    if ruta:
        ref_apertura = db.reference(f'{ruta}/apertura_caja')
        aperturas = ref_apertura.order_by_key().limit_to_last(10).get()
    else:
        print('Error al obtener aperturas')
    return aperturas


def consultar_cortes(sucursal):
    ruta = 'vistahermosa' if sucursal == 1 else 'moctezuma' if sucursal == 2 else None
    if ruta:
        ref_corte = db.reference(f'{ruta}/corte_caja')
        cortes = ref_corte.order_by_key().limit_to_last(10).get()
    else:
        print('Error al obtener aperturas')
    return cortes


def consultar_venta_historica(id,sucursal):
    ruta = 'vistahermosa' if sucursal == 1 else 'moctezuma' if sucursal == 2 else None
    if ruta:
        ref = db.reference(f"{ruta}/corte_caja/{id}/venta_historica")
        venta_historica = ref.get()
    else:
        print("Error")
    return venta_historica if venta_historica else []