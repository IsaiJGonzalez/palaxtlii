import sys
from escpos.printer import Win32Raw
import os
from django.conf import settings
from datetime import datetime,date
import locale
import firebase_service as fs

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def imprimir_retiros(suc,data):
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)
        
        #Encabezado ----
        p.text('-' * 48)
        p.set(align='center',bold=False, width=1, height=1)
        p.text('Retiro de Efectivo\n')
        p.text('-' * 48 + '\n')

        p.set(align='left',bold=False,width=1,height=1)
        #Variables
        fecha_str = data.get('fecha')
        fecha_dt = datetime.fromisoformat(fecha_str)
        fecha = fecha_dt.strftime("%d de %B de %Y a las %H:%M")
        numero_empleado = data.get('numero_empleado')
        monto = data.get('monto')
        sucursal_int = suc
        sucursal = 'Av. Palma #60, Col. Vista Hermosa, San Juan Del Río, Qro.' if sucursal_int == 1 else 'Av Moctezuma #143, Col San Cayetano, San Juan del Río, Qro.' if sucursal_int == 2 else ''
        retira = data.get('retira')
        motivo = data.get('motivo')

        p.text(f'Fecha de retiro: {fecha}\n')
        p.text(f'No. Emp: {numero_empleado}\n')
        p.text(f'Sucursal: {sucursal}\n')
        p.text('-' * 48 + '\n')
        p.text(f'Retira Empleado: {retira}\n')
        p.text(f'Motivo: {motivo}\n')
        p.text('-' * 48 + '\n')

        p.set(align='center',bold=False, width=1, height=1)

        p.text('Cantidad de Retiro:\n')
        p.text(f'$ {monto}\n\n\n\n\n')

        p.set(align='center',bold=False, width=1, height=1)
        p.text('_' * 25 + '\n')
        p.text('Firma')
        p.text('\n\n')
        p.set(align='center', bold=False)
        p.text('Este documento es evidencia del retiro de efectivo realizado. Reporte inconsistencias de inmediato.\n')
        p.cut()
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket:", e)




