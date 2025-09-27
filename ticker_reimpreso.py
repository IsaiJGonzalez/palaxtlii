import sys
from escpos.printer import Win32Raw
import os
from django.conf import settings
from datetime import datetime,date
import locale
import firebase_service as fs


def imprimir_venta(resumen):
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
        p.text(f"{resumen.get('ubicacion', '')}\n\n")
        p.text("TICKET VENTA\n")
        p.text("Cliente\n")
        p.set(align='left', bold=False, width=1, height=1)

        fecha_str = resumen.get('fecha_venta', '')
        try:
            fechaOb = datetime.strptime(fecha_str, "%Y-%m-%d")
            fecha_f = fechaOb.strftime('%d de %B de %Y')
        except:
            fecha_f = fecha_str

        p.text(f"No. Venta: {resumen.get('no_venta', '')}\n")
        p.text(f"Fecha: {fecha_f}\n")
        p.text(f"Atendió: {resumen.get('at_no_emp', '')} - {resumen.get('at_nom_emp', '')}\n")
        p.text('-' * 48 + '\n')

        # --- PRODUCTOS ---
        p.set(bold=True)
        p.text(f"{'Producto':<24}{'Cant':>6}{'P.U.':>8}{'Importe':>10}\n")
        p.set(bold=False)

        loc_emp = resumen.get('loc_emp', 0)
        productos = resumen.get('productos', [])

        for producto in productos:
            cantidad = int(producto.get('cantidad', 0))
            precio = float(producto.get('precio_unitario', 0))
            importe = float(producto.get('subtotal', 0))
            nombre = producto.get('nombre', '')

            # Si tienes IDs y funciones de nombre por ubicación
            producto_id = producto.get('productoId')
            if producto_id:
                if loc_emp == 1:
                    nombre = fs.obtener_producto_vh(producto_id)
                elif loc_emp == 2:
                    nombre = fs.obtener_producto_mc(producto_id)

            lineas_nombre = [nombre[i:i+24] for i in range(0, len(nombre), 24)]
            for i, linea in enumerate(lineas_nombre):
                if i == len(lineas_nombre) - 1:
                    p.text(f"{linea:<24}{cantidad:>6}{precio:>8.2f}{importe:>10.2f}\n")
                else:
                    p.text(f"{linea:<24}\n")

        p.text('-' * 48 + '\n')

        # --- TOTALES ---
        metodo_p = resumen.get('metodo_pago', '')
        total = float(resumen.get('total', 0))
        recibido = float(resumen.get('recibido', 0))
        cambio = float(resumen.get('cambio', 0))
        mix_ef = float(resumen.get('mix_ef', 0))
        mix_tar = float(resumen.get('mix_tar', 0))
        no_operacion = resumen.get('no_operacion', '')

        p.set(bold=False)
        p.text(f"Método de Pago: {metodo_p}\n\n")
        p.text(f"{'Total:':<20}${total:>8.2f}\n")

        if metodo_p == 'mixto':
            p.text(f"{'Tarjeta:':<20}${mix_tar:>8.2f}\n")
            p.text(f"{'Efectivo:':<20}${mix_ef:>8.2f}\n")
            p.text(f"{'Recibido:':<20}${recibido:>8.2f}\n")
            p.text(f"{'Cambio:':<20}${cambio:>8.2f}\n")
            p.text(f"Número de Operación: {no_operacion}\n\n")
        elif metodo_p == 'efectivo':
            p.text(f"{'Recibido:':<20}${recibido:>8.2f}\n")
            p.text(f"{'Cambio:':<20}${cambio:>8.2f}\n\n")
        elif metodo_p in ['tarjeta', 'transferencia']:
            p.text(f"Número de Operación: {no_operacion}\n\n")

        # --- MENSAJE FINAL ---
        p.set(align='center')
        p.text("¡Gracias por su preferencia!\n\n")
        p.text("***Reserva tu pastel perfecto***\n\n")
        p.text("Whatsapp: 427 159 0622\n")

        # --- FECHA DE IMPRESIÓN ---
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"\nFecha de impresión: {fecha_hora}\n")

        p.cut()
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket:", e)