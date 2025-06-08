from escpos.printer import Win32Raw
import os
from django.conf import settings
from datetime import datetime

def imprimir_ticket(data,loc):
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)
        
        # --- LOGO ---
        logo_path = os.path.join(settings.BASE_DIR, "static", "logo_ticket.bmp")
        if os.path.exists(logo_path):
            try:
                p.set(align='center', bold=False, width=2, height=2)
                p.image(logo_path)
            except Exception as e:
                print("⚠️ Error al imprimir logo:", e)
        else:
            print("⚠️ Logo no encontrado en:", logo_path)

        # --- ENCABEZADO ---
        p.set(align='center', bold=False, width=2, height=2)
        if(loc == 1):
            p.text('Av. Palma #60, Col. Vista Hermosa, San Juan Del Río, Qro.\n\n')
        elif(loc == 2):
            p.text('Av Moctezuma #143, Col San Cayetano, San Juan del Río, Qro.\n\n')
        p.text("TICKET DE PEDIDO\n")
        p.text("Cliente\n\n")
        p.set(align='left', bold=True, width=1, height=1)
        p.text(f"Folio: {data.get('folio', '')}\n")
        p.text(f"Cliente: {data.get('nombre_cliente', '')}\n")
        p.text(f"Teléfono: {data.get('telefono', '')}\n")
        p.text(f"Fecha de Entrega: {data.get('fecha_entrega', '')} {data.get('hora_entrega', '')}\n")
        p.text('Forma de Entrega: ')

        forma_entrega = data.get('forma_entrega')
        sucursal = data.get('sucursal')
        if(forma_entrega == "tienda"):
            p.text('Sucursal\n')
            if (sucursal == '1'):
                p.text('Av. Palma #60, Col. Vista Hermosa, San Juan Del Río, Qro.\n')
            elif(sucursal == '2'):
                p.text('Av Moctezuma #143, Col San Cayetano, San Juan del Río, Qro.\n')
        elif(forma_entrega=='envio'):
            p.text('Envio')
        p.text("----------------------------------------\n")

        # --- PRODUCTOS (formato tabla) ---
        p.set(bold=True)
        p.text(f"{'Cant':>6}{'Producto':<16}{'P.U.':>8}{'Total':>10}\n")
        p.set(bold=False)
        productos = data.get("productos", [])
        for producto in productos:
            cantidad = int(producto.get("cantidad", 0))
            nombre = producto.get("descripcion", "")[:16]
            precio = float(producto.get("precio_unitario", 0))
            total = float(producto.get('importe',0))
            p.text(f"{cantidad:>6}{nombre:<16}{precio:>8.2f}{total:>10.2f}\n")

        p.text("----------------------------------------\n")
        p.set(align='left', bold=True, width=1, height=1)
        p.text('Especificaciones: \n')
        especificaciones = data.get('especificaciones')
        p.text(especificaciones)
        p.text('\n')
        p.text("----------------------------------------\n")
        # --- TOTALES ---
        p.set(bold=True)
        p.text(f"{'Total:':<20}${data.get('total', 0):>8.2f}\n")
        p.text(f"{'Envío:':<20}${data.get('costo_envio', 0):>8.2f}\n")
        p.text(f"{'Anticipo:':<20}${data.get('anticipo', 0):>8.2f}\n")
        p.text(f"{'Recibido:':<20}${data.get('recibido', 0):>8.2f}\n")
        p.text(f"{'Cambio:':<20}${data.get('cambio', 0):>8.2f}\n")
        p.text(f"{'Total Restante:':<20}${data.get('gran_total', 0):>8.2f}\n")
        p.text("----------------------------------------\n")

        # --- MENSAJE FINAL ---
        p.set(align='center')
        no_emp = data.get('at_no_emp')
        nom_emp = data.get('at_nom_emp')
        p.text('Atendio:\n')
        p.text(no_emp )
        p.text(' - ') 
        p.text(nom_emp)
        p.text('\n')
        p.text("¡Gracias por su preferencia!\n")
        p.text("Whatsapp: 427 159 0622\n")

        # --- FECHA Y HORA DE IMPRESIÓN ---
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"\nFecha de impresión: {fecha_hora}\n")

        # --- ALIMENTAR Y CORTE ---
        p.text("\n")
        p.cut()

    except Exception as e:
        print("❌ Error general al imprimir ticket:", e)
