from django.urls import path
from . import views

urlpatterns = [
    path('',views.punto_venta,name='punto_venta')
]