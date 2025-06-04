from django.urls import path
from . import views

urlpatterns = [
    path('',views.registro_pedidos,name='registro_pedidos'),
    path('guardar_pedido/',views.guardar_pedido,name='guardar_pedido')
]