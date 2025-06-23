import sys
from escpos.printer import Win32Raw
import os
from django.conf import settings
from datetime import datetime
import json
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


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
        p.set(align='left', bold=False, width=1, height=1)
        p.text(f"Folio: {data.get('folio', '')}\n")
        p.text(f"Cliente: {data.get('nombre_cliente', '')}\n")
        p.text(f"Teléfono: {data.get('telefono', '')}\n")

        fecha_str = data.get('fecha_entrega')
        fecha_ob = datetime.strptime(fecha_str, "%Y-%m-%d")
        fecha_en = fecha_ob.strftime("%d de %B de %Y")

        p.text(f"Fecha de Entrega: {fecha_en}\n")
        p.text(f"Hora de Entrega: {data.get('hora_entrega','')} hrs.")
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
            p.text('Envio a:\n')
            direccion = data.get('direccion')
            recibe = data.get('recibe')
            cel = data.get('cel')
            referencia = data.get('referencias')
            p.text(f"{direccion}\n")
            p.text(f"Recibe: - {recibe}\n")
            p.text(f"Contacto: - {cel}\n")
            p.text(f'Referencias: {referencia}\n')
        p.text("-" * 48 + "\n")

        # --- PRODUCTOS (formato tabla) ---
        p.set(bold=True)
        p.text(f"{'Producto':<24}{'Cant':>6}{'P.U.':>8}{'Importe':>10}\n")
        p.set(bold=False)

        productos = data.get("productos", [])
        for producto in productos:
            cantidad = int(producto.get("cantidad", 0))
            nombre = producto.get("descripcion", "")
            precio = float(producto.get("precio_unitario", 0))
            total = float(producto.get("importe", 0))

            # Dividir el nombre si es muy largo en bloques de 24 caracteres
            lineas_nombre = [nombre[i:i+24] for i in range(0, len(nombre), 24)]
            for i, linea in enumerate(lineas_nombre):
                if i == len(lineas_nombre) - 1:
                    # Última línea: imprime con los datos
                    p.text(f"{linea:<24}{cantidad:>6}{precio:>8.2f}{total:>10.2f}\n")
                else:
                    # Líneas previas: solo el texto del producto
                    p.text(f"{linea:<24}\n")


        p.text("-" * 48 + "\n")
        p.set(align='left', bold=False, width=1, height=1)
        p.text('Especificaciones: \n')
        especificaciones = data.get('especificaciones')
        p.text(especificaciones)
        p.text('\n')
        p.text("-" * 48 + "\n")
        # --- TOTALES ---
        subtotal = data.get('total', 0)
        envio = data.get('costo_envio', 0)

        gSubtotal = subtotal - envio

        anticipo = str(data.get('anticipo', '0'))
        anticipo = float(anticipo) if anticipo.replace('.', '', 1).isdigit() else 0  # 

        p.set(bold=False)
        p.text(f"{'Importe Total:':<20}${gSubtotal:>8.2f}\n")
        p.text(f"{'Envío:':<20}${data.get('costo_envio', 0):>8.2f}\n")
        p.text(f"{'Subtotal:':<20}${data.get('total', 0):>8.2f}\n")
        p.text(f"{'Anticipo:':<20}${anticipo:>8.2f}\n")
        
        metodo = data.get('metodo_pago','')
        if (metodo == 'efectivo'):
            p.text(f"{'Recibido:':<20}${data.get('recibido', 0):>8.2f}\n")
            p.text(f"{'Cambio:':<20}${data.get('cambio', 0):>8.2f}\n")
        elif (metodo=='tarjeta' or metodo=='transferencia'):
            p.text('Pago con: Tarjeta / Transferencia\n')
        p.text(f"{'Total Restante:':<20}${data.get('gran_total',0):>8.2f}\n")
        p.text("-" * 48 + "\n")

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

#-- IMPRESION DEL NEGOCIO --------------------------->
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
        p.text("Negocio\n\n")
        p.set(align='left', bold=False, width=1, height=1)
        p.text(f"Folio: {data.get('folio', '')}\n")
        p.text(f"Cliente: {data.get('nombre_cliente', '')}\n")
        p.text(f"Teléfono: {data.get('telefono', '')}\n")
        p.text(f"Fecha de Entrega: {fecha_en}\n")
        p.text(f"Hora de Entrega: {data.get('hora_entrega','')} hrs.")
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
            p.text('Envio a:\n')
            direccion = data.get('direccion')
            recibe = data.get('recibe')
            cel = data.get('cel')
            referencia = data.get('referencias')
            p.text(f"{direccion}\n")
            p.text(f"Recibe: - {recibe}\n")
            p.text(f"Contacto: - {cel}\n")
            p.text(f'Referencias: {referencia}\n')
        p.text("-" * 48 + "\n")

        # --- PRODUCTOS (formato tabla) ---
        p.set(bold=True)
        p.text(f"{'Producto':<24}{'Cant':>6}{'P.U.':>8}{'Importe':>10}\n")
        p.set(bold=False)

        productos = data.get("productos", [])
        for producto in productos:
            cantidad = int(producto.get("cantidad", 0))
            nombre = producto.get("descripcion", "")
            precio = float(producto.get("precio_unitario", 0))
            total = float(producto.get("importe", 0))

            # Dividir el nombre si es muy largo en bloques de 24 caracteres
            lineas_nombre = [nombre[i:i+24] for i in range(0, len(nombre), 24)]
            for i, linea in enumerate(lineas_nombre):
                if i == len(lineas_nombre) - 1:
                    # Última línea: imprime con los datos
                    p.text(f"{linea:<24}{cantidad:>6}{precio:>8.2f}{total:>10.2f}\n")
                else:
                    # Líneas previas: solo el texto del producto
                    p.text(f"{linea:<24}\n")

        p.text("-" * 48 + "\n")
        p.set(align='left', bold=False, width=1, height=1)
        p.text('Especificaciones: \n')
        especificaciones = data.get('especificaciones')
        p.text(especificaciones)
        p.text('\n')
        p.text("-" * 48 + "\n")
        # --- TOTALES ---
        subtotal = data.get('total', 0)
        envio = data.get('costo_envio', 0)

        gSubtotal = subtotal - envio

        anticipo = str(data.get('anticipo', '0'))
        anticipo = float(anticipo) if anticipo.replace('.', '', 1).isdigit() else 0  # 

        p.set(bold=False)
        p.text(f"{'Importe Total:':<20}${gSubtotal:>8.2f}\n")
        p.text(f"{'Envío:':<20}${data.get('costo_envio', 0):>8.2f}\n")
        p.text(f"{'Subtotal:':<20}${data.get('total', 0):>8.2f}\n")
        p.text(f"{'Anticipo:':<20}${anticipo:>8.2f}\n")
        
        metodo = data.get('metodo_pago','')
        if (metodo == 'efectivo'):
            p.text(f"{'Recibido:':<20}${data.get('recibido', 0):>8.2f}\n")
            p.text(f"{'Cambio:':<20}${data.get('cambio', 0):>8.2f}\n")
        elif (metodo=='tarjeta' or metodo=='transferencia'):
            p.text('Pago con: Tarjeta / Transferencia\n')
        p.text(f"{'Total Restante:':<20}${data.get('gran_total',0):>8.2f}\n")
        p.text("-" * 48 + "\n")
        

        # --- MENSAJE FINAL ---
        p.set(align='center')
        no_emp = data.get('at_no_emp')
        nom_emp = data.get('at_nom_emp')
        p.text('Atendio:\n')
        p.text(no_emp )
        p.text(' - ') 
        p.text(nom_emp)
        p.text('\n')
        # --- FECHA Y HORA DE IMPRESIÓN ---
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"\nFecha de impresión: {fecha_hora}\n")

        # --- ALIMENTAR Y CORTE ---
        p.text("\n")
        p.cut()


        p.close()
    except Exception as e:
        print("❌ Error general al imprimir ticket:", e)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python print_ticket.py '<json>' <loc>")
        sys.exit(1)
    raw_json = sys.argv[1]
    loc = int(sys.argv[2])
    data = json.loads(raw_json)
    imprimir_ticket(data, loc)