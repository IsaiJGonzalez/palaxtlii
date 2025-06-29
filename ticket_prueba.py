from escpos.printer import Win32Raw

def imprimir_prueba():
    try:
        printer_name = "POS-80"
        p = Win32Raw(printer_name)

        p.text('Prueba de impresión.')
        p.cut()
        p.close()

    except Exception as e:
        print('Error al imprimir ticket de prueba: ',e)