from django.shortcuts import redirect

class VerificarSesionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        usuario = request.session.get("usuario")

        if usuario:
            request.usuario = usuario  # Agrega el usuario a la request para que los decoradores lo usen
        else:
            request.usuario = None  # Si no hay sesión, mantiene la request sin usuario

        return self.get_response(request)