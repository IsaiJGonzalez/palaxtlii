import sys
from escpos.printer import Win32Raw
from datetime import datetime
import locale
import time  # <--- IMPORTANTE: Necesario para la pausa

# Configuración de idioma para la fecha (intenta ponerlo en español)
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, "es_ES") # Intento alternativo para Windows
    except:
        pass # Si falla, se quedará en inglés/default

def ticket_abono(id_abono, folio, fecha, gran_total, abono, gran_total_restante, metodo_pago):
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)

        # =======================================================
        # CORRECCIÓN DE IMPRESORA (Modo Chino + Acentos)
        # =======================================================
        p._raw(b'\x1c\x2e')       # Desactivar modo Kanji/Chino
        time.sleep(0.1)           # Pequeña pausa
        p.charcode('CP850')       # Configurar idioma Español
        # =======================================================

        # Convertir fecha a formato legible
        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
            fecha_legible = fecha_dt.strftime("%d de %B de %Y, %I:%M %p")
        except:
            # Si falla el formato, usa la fecha original
            fecha_legible = fecha

        def imprimir_contenido(etiqueta):
            # --- ENCABEZADO CENTRADO ---
            p.set(align='center', bold=True)
            p.text("------------------------------------------\n")
            p.text("REPOSTERIA PALAXTLI\n")
            p.text("ABONO DE PEDIDO\n")
            p.text("------------------------------------------\n")
            
            # Etiqueta (Copia Cliente/Negocio)
            p.text(f"{etiqueta.upper()}\n")
            p.text("------------------------------------------\n")

            # --- DETALLES ALINEADOS A LA IZQUIERDA ---
            p.set(align='left', bold=False)
            p.text(f"ID:           {id_abono}\n")
            p.text(f"FOLIO:        {folio}\n")
            p.text(f"FECHA:        {fecha_legible}\n")
            p.text(f"MÉTODO PAGO:  {metodo_pago.upper()}\n")
            p.text("------------------------------------------\n")

            # --- TOTALES (Con negrita para resaltar) ---
            p.set(bold=True)
            p.text(f"{'TOTAL PEDIDO:':<20} ${gran_total:>10.2f}\n")
            p.text(f"{'ABONO REALIZADO:':<20} ${abono:>10.2f}\n")
            p.text(f"{'RESTANTE:':<20} ${gran_total_restante:>10.2f}\n")
            p.set(bold=False)
            
            p.text("------------------------------------------\n")
            p.text("\n\n")

        # 1. Ticket para NEGOCIO
        imprimir_contenido("COPIA NEGOCIO")
        p.cut()

        # 2. Ticket para CLIENTE
        imprimir_contenido("COPIA CLIENTE")
        p.cut()
        
        # Cerrar conexión
        p.close()

    except Exception as e:
        print("✖️ Error al imprimir ticket de abono:", e)