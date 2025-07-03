import sys
from escpos.printer import Win32Raw
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

def ticket_abono(id_abono, folio, fecha, gran_total, abono, gran_total_restante, metodo_pago):
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)

        # Convertir fecha a formato legible
        fecha_legible = datetime.strptime(fecha, "%Y-%m-%dT%H:%M").strftime("%d de %B de %Y, %I:%M %p")

        def imprimir_ticket(etiqueta):
            p.text("------------------------------------------\n")
            p.text("           REPOSTERIA PALAXTLI           \n")
            p.text("             ABONO DE PEDIDO                \n")
            p.text("------------------------------------------\n")
            p.text(f"{etiqueta.upper()}\n")
            p.text("------------------------------------------\n")
            p.text(f"ID:           {id_abono}\n")
            p.text(f"FOLIO:        {folio}\n")
            p.text(f"FECHA:        {fecha_legible}\n")
            p.text(f"MÉTODO PAGO:  {metodo_pago.upper()}\n")
            p.text("------------------------------------------\n")
            p.text(f"TOTAL PEDIDO:     ${gran_total:.2f}\n")
            p.text(f"ABONO REALIZADO:  ${abono:.2f}\n")
            p.text(f"RESTANTE:         ${gran_total_restante:.2f}\n")
            p.text("------------------------------------------\n")
            p.text("\n\n")

        # Ticket para NEGOCIO
        imprimir_ticket("COPIA NEGOCIO")
        # Cortar papel
        p.cut()

        # Ticket para CLIENTE
        imprimir_ticket("COPIA CLIENTE")
        # Cortar papel
        p.cut()
        p.close()

    except Exception as e:
        print("✖️ Error al imprimir ticket de abono:", e)
