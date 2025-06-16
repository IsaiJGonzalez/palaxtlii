"""
URL configuration for palaxtli project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',include('login.urls')),
    path('logout/', include('bases.urls')),
    path('menu_gerencial/', include('main_gerencial.urls')),
    path('empleados/',include('empleados.urls')),
    path('menu_cajero/',include('menu_cajero.urls')),
    path('menu_ventas/',include('menu_ventas.urls')),
    path('registro_pedidos/',include('registro_pedidos.urls')),
    path('pedidos/',include('pedidos.urls')),
    path('punto_venta/',include('punto_venta.urls')),
    path('productos/',include('productos.urls')),
    path('codigos/',include('codigos.urls')),
    path('apertura_caja/',include('apertura_caja.urls')),
    path('corte_caja/',include('corte_caja.urls'))
]
