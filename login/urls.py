from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Ruta para mostrar el login
]