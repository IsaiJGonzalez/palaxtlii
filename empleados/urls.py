from django.urls import path
from . import views

urlpatterns = [
    path('',views.empleados, name='empleados'),
    path('cambiar_contrasena',views.cambiar_contrasena,name='cambiar_contrasena')
]