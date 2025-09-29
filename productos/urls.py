from django.urls import path
from . import views


urlpatterns = [
    path('',views.productos,name='productos'),
    path('editar_producto/',views.editarProducto,name='editar_producto'),
    path('eliminarProducto/<int:sucursal_id>/<str:producto_id>/', views.eliminarProducto, name='eliminarProducto'),
]