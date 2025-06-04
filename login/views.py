from django.shortcuts import render, redirect
from firebase_config import fr_db  

def login(request):
    print("Inicio de login")

    if request.method == "POST":
        numero_empleado = request.POST.get("numero_empleado", "").strip()
        contrasena = request.POST.get("contrasena", "").strip()
        
        print(f"Buscando empleado {numero_empleado} en Firebase...")
        empleado_ref = fr_db.child("empleados").child(numero_empleado)
        empleado_data = empleado_ref.get()

        if not empleado_data:
            print("Empleado no encontrado")
            return render(request, "login.html", {"error": "Número de empleado no encontrado"})

        if str(empleado_data["contrasena"]) == contrasena:
            if(empleado_data['privilegio']) == 1:
                request.session["usuario"] = empleado_data
                return redirect("menu_gerencial")  # Redirige a todos al menú gerencial
            elif(empleado_data['privilegio'])==2:
                request.session["usuario"] = empleado_data
                return redirect("menu_ventas")
            elif(empleado_data['privilegio'])==3:
                request.session["usuario"] = empleado_data
                return redirect("punto_venta")
        else:
            print("Contraseña incorrecta")
            return render(request, "login.html", {"error": "Credenciales incorrectas"})

    return render(request, "login.html")