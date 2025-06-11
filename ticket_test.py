from escpos.printer import Win32Raw

try:
    p = Win32Raw("POS-80")
    p.text("Ticket de prueba\n")
    p.cut()
    p.close()
except Exception as e:
    print("Error:", e)
