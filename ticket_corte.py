import sys
from escpos.printer import Win32Raw
import os
from datetime import datetime
import locale
import time  # <--- Necesario para la pausa

# Configuración de idioma segura para Windows
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, "es_ES")
    except:
        pass


def imprimir_corte(data, nombre_emp, suc, monto_apertura):
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

        # Función auxiliar para imprimir filas alineadas
        def print_row(label, amount, bold=False):
            p.set(bold=bold)
            p.text(f"{label:<28} $ {amount:>10.2f}\n")

        # >>> SITIO ESTRATÉGICO: MONTO DE APERTURA <<<
        # Se coloca antes de los ingresos para establecer la base de la caja
        print_row("MONTO DE APERTURA:", float(monto_apertura), bold=True)
        p.text('-' * 48 + '\n')

        # --- DATOS FINANCIEROS ---
        ventas = data.get('ventas', {})
        pedidos = data.get('pedidos', {})
        retiros = data.get('retiros', 0)
        total_en_caja = data.get('total_en_caja', 0)
        esperado_en_caja = data.get('esperado_en_caja', 0)
        diferencia = data.get('diferencia', 0)

        # --- DATOS DE DESCUENTOS ---
        cant_descuentos = int(ventas.get('cantidad_descuentos_aplicados', 0))
        total_descontado = float(ventas.get('total_descontado_dinero', 0))

        p.set(bold=True, align='left')
        p.text('INGRESOS:\n\n')
        
        # 1. VENTAS
        p.set(bold=True)
        p.text('Ventas:\n')
        p.set(bold=False)
        print_row("  Efectivo:", ventas.get("efectivo", 0))
        print_row("  Transferencia:", ventas.get("transferencia", 0))
        print_row("  Tarjeta:", ventas.get("tarjeta", 0))

        # SECCIÓN DE DESCUENTOS
        if cant_descuentos > 0:
            p.text('\n') 
            p.set(bold=True)
            p.text('  Metricas de Descuento:\n') 
            p.set(bold=False)
            p.text(f"    Cant. Aplicados:            {cant_descuentos}\n")
            print_row("    Monto Condonado:", total_descontado)
            p.text('\n')

        # 2. PEDIDOS
        p.set(bold=True)
        p.text('Pedidos:\n')
        p.set(bold=False)
        print_row("  Efectivo:", pedidos.get("efectivo", 0))
        print_row("  Transferencia:", pedidos.get("transferencia", 0))
        print_row("  Tarjeta:", pedidos.get("tarjeta", 0))

        p.text('-' * 48 + '\n')
        print_row("Retiros:", retiros)
        p.text('-' * 48 + '\n')

        # --- TOTALES FINALES ---
        # Total en caja es lo que el usuario contó
        print_row("Total en Caja:", total_en_caja, bold=True)
        # Total esperado es (Apertura + Ventas Efectivo + Pedidos Efectivo - Retiros)
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

        p.set(align='center', font='a') 
        p.text('Este documento es evidencia del corte de caja correspondiente a la fecha indicada.\n')
        p.text('Reporte inconsistencias de inmediato.\n')
        p.text('\n')
        
        p.cut()
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket de corte:", e)