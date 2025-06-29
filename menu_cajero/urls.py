from django.urls import path
from . import views

urlpatterns = [
    path('',views.menu_cajero,name='menu_cajero'),
    path('impresion_prueba/',views.impresion_prueba,name='impresion_prueba')
]