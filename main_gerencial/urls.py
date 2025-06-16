from django.urls import path
from . import views

urlpatterns = [
    path('',views.main_gerencial, name='menu_gerencial'),
    path('entregar_pedido/',views.actualizar_pedido_estado,name="entregar_pedido")
]