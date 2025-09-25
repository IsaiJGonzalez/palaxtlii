from django.urls import path
from . import views

urlpatterns = [
    path('',views.historial_caja,name='historial_cajas'),
    path('ver_ventas/<str:id>/', views.ver_ventas, name='ver_ventas'),
]
