from django.shortcuts import render, redirect
from django.contrib import messages
import firebase_service as fs 

def registro_tarjetas(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            descuento = float(request.POST.get('descuento'))
            tipo = request.POST.get('tipo')
            existencias = int(request.POST.get('existencias'))
            activo = request.POST.get('activo') == 'on'

            fs.crear_tarjeta_descuento(codigo, descuento, tipo, existencias, activo)
            
            messages.success(request, f"Tarjeta '{codigo}' registrada correctamente.")
            return redirect('registro_tarjetas')
        except ValueError:
            messages.error(request, "Error en los datos. Revisa los valores numéricos.")
    
    # Obtenemos las tarjetas para mostrarlas en la tabla
    tarjetas = fs.obtener_tarjetas_descuento()
    
    return render(request, 'registro_tarjetas.html', {'tarjetas': tarjetas})