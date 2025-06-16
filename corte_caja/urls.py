from django.urls import path
from . import views

urlpatterns = [
    path('',views.corte_caja,name='corte_caja')
]