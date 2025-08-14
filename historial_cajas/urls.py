from django.urls import path
from . import views

urlpatterns = [
    path('',views.historial_caja,name='historial_cajas')
]
