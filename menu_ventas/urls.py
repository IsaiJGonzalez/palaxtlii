from django.urls import path
from . import views

urlpatterns = [
    path('',views.menu_ventas,name='menu_ventas')
]