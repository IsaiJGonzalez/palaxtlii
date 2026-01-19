from escpos.printer import Win32Raw
import time  # <--- No olvides importar time

def imprimir_prueba():
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)

        # =======================================================
        # CORRECCIÓN DE IMPRESORA (Modo Chino + Acentos)
        # =======================================================
        p._raw(b'\x1c\x2e')       # Comando para desactivar modo Chino
        time.sleep(0.1)           # Pausa técnica necesaria
        p.charcode('CP850')       # Configurar idioma Español
        # =======================================================

        p.text('Prueba de impresión.\n') # Agregué \n para que no quede pegado al corte
        
        p.cut()
        p.close()

    except Exception as e:
        print('Error al imprimir ticket de prueba: ',e)