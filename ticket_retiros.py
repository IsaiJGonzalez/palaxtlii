import sys
from escpos.printer import Win32Raw
import os
from datetime import datetime
import locale
import time  # <--- IMPORTANTE: Necesario para la pausa

# Configuración segura de idioma
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, "es_ES")
    except:
        pass

def imprimir_retiros(suc, data):
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
        p.text('RETIRO DE EFECTIVO\n')
        p.text('-' * 48 + '\n')

        p.set(align='left', bold=False)

        # Variables
        fecha_str = data.get('fecha')
        try:
            fecha_dt = datetime.fromisoformat(fecha_str)
            fecha_fmt = fecha_dt.strftime("%d de %B de %Y a las %H:%M")
        except:
            fecha_fmt = fecha_str

        numero_empleado = data.get('numero_empleado')
        monto = data.get('monto')
        retira = data.get('retira')
        motivo = data.get('motivo')

        # Dirección con saltos de línea para que no se corte feo
        sucursal_int = suc
        if sucursal_int == 1:
            sucursal = 'Av. Palma #60, Col. Vista Hermosa,\nSan Juan Del Río, Qro.'
        elif sucursal_int == 2:
            sucursal = 'Av. Moctezuma #143, Col. San Cayetano,\nSan Juan del Río, Qro.'
        else:
            sucursal = ''

        p.text(f'Fecha:    {fecha_fmt}\n')
        p.text(f'No. Emp:  {numero_empleado}\n')
        p.text(f'Sucursal: {sucursal}\n')
        p.text('-' * 48 + '\n')
        
        p.text(f'Retira:   {retira}\n')
        p.text(f'Motivo:   {motivo}\n')
        p.text('-' * 48 + '\n')

        # --- MONTO RESALTADO ---
        p.set(align='center', bold=False)
        p.text('Cantidad Retirada:\n')
        
        # Doble tamaño y negrita para el dinero
        p.set(align='center', bold=True, width=2, height=2)
        p.text(f"$ {monto}\n")
        
        p.set(align='center', bold=False, width=1, height=1)
        p.text('\n\n\n\n') # Espacio para firma

        # --- FIRMA ---
        p.text('_' * 25 + '\n')
        p.text('Firma de quien retira\n\n')
        
        p.set(align='center', font='a') # Letra pequeña para el texto legal
        p.text('Este documento es evidencia del retiro de efectivo realizado.\n')
        p.text('Reporte inconsistencias de inmediato.\n')
        p.text('\n')
        
        p.cut()
        p.close()

    except Exception as e:
        print("❌ Error general al imprimir ticket de retiro:", e)