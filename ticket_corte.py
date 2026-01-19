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
import sys
from escpos.printer import Win32Raw
import os
from datetime import datetime
import locale
import time  # <--- AGREGADO: Necesario para la pausa

# Configuración de idioma segura para Windows
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, "es_ES")
    except:
        pass

def imprimir_corte(data, nombre_emp, suc):
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

        # --- ENCABEZADO ---
        p.set(align='center', bold=True)
        p.text('-' * 48 + '\n')
        p.text('CORTE DE CAJA\n')
        p.text('-' * 48 + '\n')

        p.set(align='left', bold=False)

        # Variables de Fecha y Sucursal
        fecha_str = data.get('fecha_corte')
        try:
            fecha_dt = datetime.fromisoformat(fecha_str)
            fecha_fmt = fecha_dt.strftime("%d de %B de %Y a las %H:%M")
        except:
            fecha_fmt = fecha_str

        numero_emp = data.get('no_emp')
        
        sucursal_int = suc
        if sucursal_int == 1:
            sucursal = 'Av. Palma #60, Col. Vista Hermosa,\nSan Juan Del Río, Qro.'
        elif sucursal_int == 2:
            sucursal = 'Av. Moctezuma #143, Col. San Cayetano,\nSan Juan del Río, Qro.'
        else:
            sucursal = ''

        p.text(f'Cierre:   {fecha_fmt}\n')
        p.text(f'No. Emp:  {numero_emp}\n')
        p.text(f'Nombre:   {nombre_emp}\n')
        p.text(f'Sucursal: {sucursal}\n')
        p.text('-' * 48 + '\n')

        # --- DATOS FINANCIEROS ---
        ventas = data.get('ventas', {})
        pedidos = data.get('pedidos', {})
        retiros = data.get('retiros', 0)
        total_en_caja = data.get('total_en_caja', 0)
        esperado_en_caja = data.get('esperado_en_caja', 0)
        diferencia = data.get('diferencia', 0)

        # Función auxiliar para imprimir filas alineadas
        # Formato: Texto a la izquierda (30 chars) | Dinero a la derecha (10 chars)
        def print_row(label, amount, bold=False):
            p.set(bold=bold)
            p.text(f"{label:<28} $ {amount:>10.2f}\n")

        p.set(bold=True, align='left')
        p.text('INGRESOS:\n\n')
        
        p.set(bold=True)
        p.text('Ventas:\n')
        p.set(bold=False)
        print_row("  Efectivo:", ventas.get("efectivo", 0))
        print_row("  Transferencia:", ventas.get("transferencia", 0))
        print_row("  Tarjeta:", ventas.get("tarjeta", 0))

        p.set(bold=True)
        p.text('\nPedidos:\n')
        p.set(bold=False)
        print_row("  Efectivo:", pedidos.get("efectivo", 0))
        print_row("  Transferencia:", pedidos.get("transferencia", 0))
        print_row("  Tarjeta:", pedidos.get("tarjeta", 0))

        p.text('-' * 48 + '\n')
        print_row("Retiros:", retiros)
        p.text('-' * 48 + '\n')

        # --- TOTALES FINALES (En Negrita) ---
        print_row("Total en Caja:", total_en_caja, bold=True)
        print_row("Total Esperado:", esperado_en_caja, bold=True)
        
        # Diferencia
        diferencia_abs = abs(diferencia)
        p.text('\n')
        if diferencia < 0:
            p.set(bold=True)
            p.text(f"{'Diferencia (SOBRANTE):':<28} $ {diferencia_abs:>10.2f}\n")
        elif diferencia > 0:
            p.set(bold=True)
            p.text(f"{'Diferencia (FALTANTE):':<28} $ {diferencia_abs:>10.2f}\n")
        else:
            print_row("Diferencia:", 0.00, bold=True)

        # --- PIE DE PÁGINA ---
        p.text('\n\n\n\n\n')
        p.set(align='center', bold=False)
        p.text('_' * 25 + '\n')
        p.text('Firma Responsable\n\n')

        p.set(align='center', font='a') # Letra un poco más chica para el legal
        p.text('Este documento es evidencia del corte de caja correspondiente a la fecha indicada.\n')
        p.text('Reporte inconsistencias de inmediato.\n')
        p.text('\n')
        
        p.cut()
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket de corte:", e)