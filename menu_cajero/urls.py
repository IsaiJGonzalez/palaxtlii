from django.urls import path
from . import views

urlpatterns = [
    path('',views.menu_cajero,name='menu_cajero')
]