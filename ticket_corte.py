import sys
from escpos.printer import Win32Raw
import os
from django.conf import settings
from datetime import datetime, date
import locale
import firebase_service as fs

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def imprimir_corte(data, nombre_emp, suc):
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)
        
        # Encabezado
        p.text('-' * 48)
        p.set(align='center', bold=False, width=1, height=1)
        p.text('Corte de Caja\n')
        p.text('-' * 48 + '\n')

        p.set(align='left', bold=False, width=1, height=1)

        # Variables
        fecha_str = data.get('fecha_corte')
        fecha_dt = datetime.fromisoformat(fecha_str)
        fecha = fecha_dt.strftime("%d de %B de %Y a las %H:%M")
        numero_emp = data.get('no_emp')
        sucursal_int = suc
        sucursal = 'Av. Palma #60, Col. Vista Hermosa, San Juan Del Río, Qro.' if sucursal_int == 1 else 'Av. Moctezuma #143, Col. San Cayetano, San Juan del Río, Qro.' if sucursal_int == 2 else ''

        p.text(f'Fecha de Cierre: {fecha}\n')
        p.text(f'No. Emp: {numero_emp}\n')
        p.text(f'Nombre: {nombre_emp}\n')
        p.text(f'Sucursal: {sucursal}\n')
        p.text('-' * 48 + '\n')

        # Ingresos
        ventas = data.get('ventas', {})
        pedidos = data.get('pedidos', {})
        retiros = data.get('retiros', 0)
        total_en_caja = data.get('total_en_caja', 0)
        esperado_en_caja = data.get('esperado_en_caja', 0)
        diferencia = data.get('diferencia', 0)

        p.text('Ingresos:\n\n')
        p.text('Ventas:\n')
        p.text(f'  Efectivo:        $ {ventas.get("efectivo", 0):.2f}\n')
        p.text(f'  Transferencia:   $ {ventas.get("transferencia", 0):.2f}\n')
        p.text(f'  Tarjeta:         $ {ventas.get("tarjeta", 0):.2f}\n')

        p.text('\nPedidos:\n')
        p.text(f'  Efectivo:        $ {pedidos.get("efectivo", 0):.2f}\n')
        p.text(f'  Transferencia:   $ {pedidos.get("transferencia", 0):.2f}\n')
        p.text(f'  Tarjeta:         $ {pedidos.get("tarjeta", 0):.2f}\n')

        p.text('-' * 48 + '\n')
        p.text(f'Retiros:           $ {retiros:.2f}\n')
        p.text('-' * 48 + '\n')

        p.text(f'Total en Caja:     $ {total_en_caja:.2f}\n')
        p.text(f'Total Esperado:    $ {esperado_en_caja:.2f}\n')
        
        # Mostrar diferencia con condición
        diferencia_abs = abs(diferencia)
        if diferencia < 0:
            p.text(f'Diferencia:        Sobrante $ {diferencia_abs:.2f}\n')
        elif diferencia > 0:
            p.text(f'Diferencia:        Faltante $ {diferencia_abs:.2f}\n')
        else:
            p.text('Diferencia:         $ 0.00\n')

        # Firma y leyenda
        p.text('\n\n\n\n\n')
        p.set(align='center', bold=False)
        p.text('_' * 25 + '\n')
        p.text('Firma\n\n')

        p.text('Este documento es evidencia del corte de caja correspondiente a la fecha y empleada/o indicados. \n')
        p.text('Reporte inconsistencias de inmediato.\n')
        p.text('\n')
        p.cut()
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket:", e)
