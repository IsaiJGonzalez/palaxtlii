from django.shortcuts import render

# Create your views here.
def corte_caja(request):
    privilegio = request.session.get('usuario',{}).get('privilegio',0)

    if privilegio == 1:
        base = 'base_gerencial.html'
    elif privilegio == 2:
        base = 'base_ventas.html'
    elif privilegio == 2:
        base = 'base_cajero.html'

    context = {
        'base':base
    }

    return render(request,'corte_caja.html',context)