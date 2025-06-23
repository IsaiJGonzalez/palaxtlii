import sys
from escpos.printer import Win32Raw
import os
from django.conf import settings
from datetime import datetime,date
import locale
import firebase_service as fs

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

def imprimir_venta(resumen):
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)
        
        #Ticket Cliente
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
        
        #Encabezado ----
        p.set(align='center',bold=False, width=2, height=2)
        ubicacion = resumen.get('ubicacion')
        p.text(f'{ubicacion}\n\n')
        p.text('TICKET VENTA\n')
        p.text('Cliente\n')
        p.set(align='left',bold=False,width=1,height=1)
        
        no_venta = resumen.get('no_venta')
        
        fecha_str = resumen.get('fecha_venta')
        fechaOb = datetime.strptime(fecha_str, "%Y-%m-%d")
        fecha_f = fechaOb.strftime('%d de %B de %Y')

        atendio_nom = resumen.get('at_nom_emp')
        atendio_num = resumen.get('at_no_emp')
        
        p.text(f'No. Venta: {no_venta}\n')
        p.text(f'Fecha: {fecha_f}\n')
        p.text(f'Atendio: {atendio_num} - {atendio_nom}\n')

        p.text('-' * 48 + '\n')

                # --- PRODUCTOS (formato tabla) ---
        p.set(bold=True)
        p.text(f"{'Producto':<24}{'Cant':>6}{'P.U.':>8}{'Importe':>10}\n")
        p.set(bold=False)

        loc_emp = resumen.get('loc_emp')

        productos = resumen.get('productos',[])
        for producto in productos:
            cantidad = producto.get('cantidad',0)
            producto_id = producto.get('productoId')
            if (loc_emp == 1):
                nombre = fs.obtener_producto_vh(producto_id)
            elif(loc_emp == 2):
                nombre = fs.obtener_producto_mc(producto_id)
            precio = producto.get('precio_unitario',0.0)
            importe = producto.get('subtotal',0.0)

            #dividimos el nombre
            lineas_nombre = [nombre[i:i+24] for i in range(0, len(nombre),24)]
            for i, linea in enumerate(lineas_nombre):
                if i == len(lineas_nombre) - 1:
                    p.text(f'{linea:<24}{cantidad:>6}{precio:>8.2f}{importe:>10.2f}\n')
                else:
                    p.text(f"{linea:<24}\n")

        p.text('-'*48+'\n')

        #Totales
        total = resumen.get('total',0.0)
        metodo_p = resumen.get('metodo_pago')
        recibido = resumen.get('recibido',0.0)
        cambio = resumen.get('cambio',0.0)
        no_operacion = resumen.get('no_operacion','')

        p.set(bold=False)
        p.text(f'Método de Pago: {metodo_p}\n\n')
        p.text(f"{'Total:':<20}${total:>8.2f}\n")
        if metodo_p == 'efectivo':
            p.text(f"{'Recibido:':<20}${recibido:>8.2f}\n")
            p.text(f"{'Cambio:':<20}${cambio:>8.2f}\n\n")
        elif metodo_p == 'tarjeta' or metodo_p == 'transferencia':
            p.set(f'Número de Operación: {no_operacion}\n\n')
        

        #Mensaje final
        p.set(align='center')
        p.text("¡Gracias por su preferencia!\n\n")
        p.text('***Reserva tu pastel perfecto***\n\n')
        p.text("Whatsapp: 427 159 0622\n")

        p.text('\n')
        # --- FECHA Y HORA DE IMPRESIÓN ---
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"\nFecha de impresión: {fecha_hora}\n")

        p.cut()

        #Ticket Negocio
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
        
        #Encabezado ----
        p.set(align='center',bold=False, width=2, height=2)
        ubicacion = resumen.get('ubicacion')
        p.text(f'{ubicacion}\n')
        p.text('TICKET VENTA\n')
        p.text('Negocio\n')
        p.set(align='left',bold=False,width=1,height=1)
        
        no_venta = resumen.get('no_venta')
        
        fecha_str = resumen.get('fecha_venta')
        fechaOb = datetime.strptime(fecha_str, "%Y-%m-%d")
        fecha_f = fechaOb.strftime('%d de %B de %Y')

        atendio_nom = resumen.get('at_nom_emp')
        atendio_num = resumen.get('at_no_emp')
        
        p.text(f'No. Venta: {no_venta}\n')
        p.text(f'Fecha: {fecha_f}\n')
        p.text(f'Atendio: {atendio_num} - {atendio_nom}\n')

        p.text('-' * 48 + '\n')

                # --- PRODUCTOS (formato tabla) ---
        p.set(bold=True)
        p.text(f"{'Producto':<24}{'Cant':>6}{'P.U.':>8}{'Importe':>10}\n")
        p.set(bold=False)

        loc_emp = resumen.get('loc_emp')

        productos = resumen.get('productos',[])
        for producto in productos:
            cantidad = producto.get('cantidad',0)
            producto_id = producto.get('productoId')
            if (loc_emp == 1):
                nombre = fs.obtener_producto_vh(producto_id)
            elif(loc_emp == 2):
                nombre = fs.obtener_producto_mc(producto_id)
            precio = producto.get('precio_unitario')
            importe = producto.get('subtotal')

            #dividimos el nombre
            lineas_nombre = [nombre[i:i+24] for i in range(0, len(nombre),24)]
            for i, linea in enumerate(lineas_nombre):
                if i == len(lineas_nombre) - 1:
                    p.text(f'{linea:<24}{cantidad:>6}{precio:>8.2f}{importe:>10.2f}\n')
                else:
                    p.text(f"{linea:<24}\n")

        p.text('-'*48+'\n')

        #Totales
        total = resumen.get('total',0.0)
        metodo_p = resumen.get('metodo_pago')
        recibido = resumen.get('recibido',0.0)
        cambio = resumen.get('cambio',0.0)
        no_operacion = resumen.get('no_operacion','')

        p.set(bold=False)
        p.text(f'Método de Pago: {metodo_p}\n\n')
        p.text(f"{'Total:':<20}${total:>8.2f}\n")
        if metodo_p == 'efectivo':
            p.text(f"{'Recibido:':<20}${recibido:>8.2f}\n")
            p.text(f"{'Cambio:':<20}${cambio:>8.2f}\n\n")
        elif metodo_p == 'tarjeta' or metodo_p == 'transferencia':
            p.set(f'Número de Operación: {no_operacion}\n\n')

        p.text('\n')
        # --- FECHA Y HORA DE IMPRESIÓN ---
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"\nFecha de impresión: {fecha_hora}\n")

        p.cut()
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket:", e)


