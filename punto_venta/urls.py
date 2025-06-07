from django.urls import path
from . import views

urlpatterns = [
    path('',views.punto_venta,name='punto_venta'),
    path('registrar_venta/',views.registrar_venta,name='registrar_venta')
]