from django.shortcuts import redirect
from functools import wraps

def requiere_privilegio(privilegios_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            usuario = request.session.get("usuario")

            if usuario and usuario.get("privilegio") in privilegios_permitidos:
                return view_func(request, *args, **kwargs)

            return redirect("login")
        return _wrapped_view
    return decorador


def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        usuario = request.session.get("usuario")

        if usuario:
            return view_func(request, *args, **kwargs)

        return redirect("login")  # Si no ha iniciado sesión, lo redirige
    return _wrapped_view



# Decoradores específicos
gerente_required = requiere_privilegio([1])  # Solo gerente
ventas_required = requiere_privilegio([2])   # Solo ventas
cajero_required = requiere_privilegio([3])   # Solo cajero


# Decorador para gerente y ventas
gerente_ventas_required = requiere_privilegio([1, 2])