from django.urls import path
from . import views

urlpatterns = [
    path('',views.visor_ventas,name='visor_ventas')
]