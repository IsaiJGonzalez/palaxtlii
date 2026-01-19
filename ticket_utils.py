import sys
from escpos.printer import Win32Raw
import os
from django.conf import settings
from datetime import datetime
import json
import locale
import time  # <--- NECESARIO para la pausa

# Configuración de locale segura
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, "es_ES")
    except:
        pass

def imprimir_ticket(data, loc):
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)
        
        # =======================================================
        # CORRECCIÓN DE IMPRESORA (Modo Chino + Acentos)
        # =======================================================
        p._raw(b'\x1c\x2e')       # Desactivar modo Kanji/Chino
        time.sleep(0.1)           # Pausa técnica
        p.charcode('CP850')       # Configurar idioma Español
        # =======================================================

        # Función interna para imprimir el contenido (evita duplicar código)
        def imprimir_contenido(titulo_seccion):
            # --- LOGO ---
            logo_path = os.path.join(settings.BASE_DIR, "static", "logo_ticket.bmp")
            if os.path.exists(logo_path):
                try:
                    p.set(align='center', bold=False, width=2, height=2)
                    p.image(logo_path)
                except Exception as e:
                    pass # Ignorar error de logo para no detener impresión

            # --- ENCABEZADO ---
            p.set(align='center', bold=False, width=2, height=2)
            
            # Dirección de la sucursal emisora
            if loc == 1:
                p.text('Av. Palma #60, Col. Vista Hermosa,\nSan Juan Del Río, Qro.\n\n')
            elif loc == 2:
                p.text('Av Moctezuma #143, Col San Cayetano,\nSan Juan del Río, Qro.\n\n')
            
            p.text("TICKET DE PEDIDO\n")
            p.text(f"{titulo_seccion}\n\n") # Cliente o Negocio
            
            # --- DATOS GENERALES ---
            p.set(align='left', bold=False, width=1, height=1)
            p.text(f"Folio:    {data.get('folio', '')}\n")
            p.text(f"Cliente:  {data.get('nombre_cliente', '')}\n")
            p.text(f"Teléfono: {data.get('telefono', '')}\n")

            # Fecha de entrega
            fecha_str = data.get('fecha_entrega')
            try:
                fecha_ob = datetime.strptime(fecha_str, "%Y-%m-%d")
                fecha_en = fecha_ob.strftime("%d de %B de %Y")
            except:
                fecha_en = fecha_str

            p.text(f"Entrega:  {fecha_en}\n")
            p.text(f"Hora:     {data.get('hora_entrega','')} hrs.\n")
            p.text('-' * 48 + '\n')

            # --- FORMA DE ENTREGA ---
            p.text('Detalles de Entrega:\n')
            forma_entrega = data.get('forma_entrega')
            sucursal_entrega = str(data.get('sucursal'))

            if forma_entrega == "tienda":
                p.text('RECOGE EN SUCURSAL:\n')
                if sucursal_entrega == '1':
                    p.text('Av. Palma #60, Col. Vista Hermosa\n')
                elif sucursal_entrega == '2':
                    p.text('Av Moctezuma #143, Col San Cayetano\n')
            
            elif forma_entrega == 'envio':
                p.text('ENVÍO A DOMICILIO:\n')
                direccion = data.get('direccion', '')
                recibe = data.get('recibe', '')
                cel = data.get('cel', '')
                referencia = data.get('referencias', '')
                
                p.text(f"Dir: {direccion}\n")
                if recibe: p.text(f"Recibe: {recibe}\n")
                if cel: p.text(f"Tel: {cel}\n")
                if referencia: p.text(f"Ref: {referencia}\n")
            
            p.text("-" * 48 + "\n")

            # --- PRODUCTOS ---
            p.set(bold=True)
            p.text(f"{'Producto':<24}{'Cant':>6}{'P.U.':>8}{'Total':>10}\n")
            p.set(bold=False)

            productos = data.get("productos", [])
            for producto in productos:
                try:
                    cantidad = int(producto.get("cantidad", 0))
                    precio = float(producto.get("precio_unitario", 0))
                    total_prod = float(producto.get("importe", 0))
                    nombre = producto.get("descripcion", "")
                except:
                    continue

                lineas_nombre = [nombre[i:i+24] for i in range(0, len(nombre), 24)]
                for i, linea in enumerate(lineas_nombre):
                    if i == len(lineas_nombre) - 1:
                        p.text(f"{linea:<24}{cantidad:>6}{precio:>8.2f}{total_prod:>10.2f}\n")
                    else:
                        p.text(f"{linea:<24}\n")

            p.text("-" * 48 + "\n")

            # --- ESPECIFICACIONES ---
            especificaciones = data.get('especificaciones')
            if especificaciones:
                p.text('Especificaciones:\n')
                p.text(f"{especificaciones}\n")
                p.text("-" * 48 + "\n")

            # --- CALCULOS DE TOTALES ---
            try:
                subtotal_raw = float(data.get('total', 0))
                costo_envio = float(data.get('costo_envio', 0))
                gSubtotal = subtotal_raw - costo_envio
                
                anticipo_str = str(data.get('anticipo', '0'))
                # Limpieza simple de anticipo
                if anticipo_str.replace('.', '', 1).isdigit():
                    anticipo = float(anticipo_str)
                else:
                    anticipo = 0.0

                gran_total = float(data.get('gran_total', 0))
            except:
                gSubtotal = 0
                costo_envio = 0
                anticipo = 0
                gran_total = 0

            # Impresión de Totales
            p.set(bold=False)
            p.text(f"{'Importe Productos:':<20}${gSubtotal:>8.2f}\n")
            p.text(f"{'Costo Envío:':<20}${costo_envio:>8.2f}\n")
            p.text(f"{'Subtotal Ticket:':<20}${subtotal_raw:>8.2f}\n")
            p.text(f"{'Anticipo:':<20}${anticipo:>8.2f}\n")
            
            # --- MÉTODO DE PAGO ---
            metodo = data.get('metodo_pago', '').lower()
            p.text("-" * 48 + "\n")
            p.text(f"Método de pago: {metodo.upper()}\n")

            if metodo == 'mixto':
                try:
                    mix_tar = float(data.get('mix_tar', 0))
                    mix_ef = float(data.get('mix_ef', 0))
                    p.text(f"{'Tarjeta:':<20}${mix_tar:>8.2f}\n")
                    p.text(f"{'Efectivo:':<20}${mix_ef:>8.2f}\n")
                except:
                    pass
            
            if metodo in ['mixto', 'tarjeta', 'transferencia']:
                num_op = str(data.get('num_operacion', ''))
                if num_op:
                    p.text(f"No. Operación: {num_op}\n")

            if metodo in ['efectivo', 'mixto']:
                try:
                    recibido = float(data.get('recibido', 0))
                    cambio = float(data.get('cambio', 0))
                    p.text(f"{'Recibido:':<20}${recibido:>8.2f}\n")
                    p.text(f"{'Cambio:':<20}${cambio:>8.2f}\n")
                except:
                    pass

            # Total Restante en Grande
            p.set(bold=True)
            p.text(f"{'TOTAL RESTANTE:':<20}${gran_total:>8.2f}\n")
            p.set(bold=False)
            p.text("-" * 48 + "\n")

            # --- PIE DE TICKET ---
            p.set(align='center')
            no_emp = data.get('at_no_emp', '')
            nom_emp = data.get('at_nom_emp', '')
            p.text(f'Atendió: {no_emp} - {nom_emp}\n')
            
            p.text("¡Gracias por su preferencia!\n")
            p.text("Whatsapp: 427 159 0622\n")
            
            fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            p.text(f"\nImpreso: {fecha_hora}\n")
            
            # Espacio final y corte
            p.text("\n\n")

        # 1. IMPRIMIR COPIA CLIENTE
        imprimir_contenido("COPIA CLIENTE")
        p.cut()

        # 2. IMPRIMIR COPIA NEGOCIO
        imprimir_contenido("COPIA NEGOCIO")
        p.cut()

        # CERRAR CONEXIÓN
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket:", e)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python print_ticket.py '<json>' <loc>")
        sys.exit(1)
    
    raw_json = sys.argv[1]
    try:
        loc_arg = int(sys.argv[2])
    except:
        loc_arg = 1
        
    try:
        data_parsed = json.loads(raw_json)
        imprimir_ticket(data_parsed, loc_arg)
    except json.JSONDecodeError as e:
        print("❌ Error al decodificar JSON:", e)