from django.urls import path
from . import views 

urlpatterns = [
    path('',views.pedidos,name='pedidos'),
    path('act_pedido_estado/',views.act_pedido_estado, name='estado_pedido')
]