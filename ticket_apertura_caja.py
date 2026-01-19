import sys
from escpos.printer import Win32Raw
import os
from datetime import datetime
import locale
import time  # <--- IMPORTANTE: Necesario para la pausa

# Configuración segura de idioma para fechas
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, "es_ES")
    except:
        pass

def imprimir_apertura(data):
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

        # --- ENCABEZADO ---
        p.set(align='center', bold=True)
        p.text('-' * 48 + '\n')
        p.text('APERTURA DE CAJA\n')
        p.text('-' * 48 + '\n')

        # --- DATOS DEL EMPLEADO ---
        p.set(align='left', bold=False)
        
        # Procesamiento de fecha
        fecha_str = data.get('fecha')
        try:
            fecha_dt = datetime.fromisoformat(fecha_str)
            fecha_fmt = fecha_dt.strftime("%d de %B de %Y a las %H:%M")
        except:
            fecha_fmt = fecha_str

        nombre_emp = data.get('nombre', 'Desconocido')
        numero_emp = data.get('no_emp', 'S/N')
        fondo = data.get('fondo', '0.00')
        
        # Lógica de sucursal
        sucursal_int = data.get('sucursal')
        if sucursal_int == 1:
            sucursal = 'Av. Palma #60, Col. Vista Hermosa,\nSan Juan Del Río, Qro.'
        elif sucursal_int == 2:
            sucursal = 'Av Moctezuma #143, Col San Cayetano,\nSan Juan del Río, Qro.'
        else:
            sucursal = 'Sucursal Desconocida'

        p.text(f'Fecha:    {fecha_fmt}\n')
        p.text(f'No. Emp:  {numero_emp}\n')
        p.text(f'Nombre:   {nombre_emp}\n')
        p.text('-' * 48 + '\n')
        p.text(f'Sucursal: {sucursal}\n')
        p.text('-' * 48 + '\n')

        # --- FONDO RECIBIDO (RESALTADO) ---
        p.set(align='center', bold=False)
        p.text('Recibí el fondo inicial de:\n')
        
        # El dinero va en grande y negrita
        p.set(align='center', bold=True, width=2, height=2)
        p.text(f"$ {fondo}\n")
        
        # Resetear tamaño
        p.set(align='center', bold=False, width=1, height=1)
        p.text('\n\n\n\n') # Espacio para firmar

        # --- FIRMA ---
        p.text('_' * 25 + '\n')
        p.text('Firma Responsable\n\n')
        
        p.set(align='center', bold=False)
        p.text('Este documento es evidencia del fondo\nentregado. Reporte inconsistencias.\n')
        
        p.cut()
        p.close()
        
    except Exception as e:
        print("❌ Error general al imprimir ticket de apertura:", e)