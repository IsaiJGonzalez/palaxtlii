from django.shortcuts import render, redirect

# Create your views here.

def logout(request):
    request.session.flush()
    print('sesion cerrada')
    return redirect('login')

def base_gerencial(request):
    nombre_empleado = request.session.get('usuario',{}).get('nombre','usuario')
    return render(request, 'base_gerencial.html' ,{'nombre_empleado':nombre_empleado})