from django.urls import path
from . import views


urlpatterns = [
    path('',views.registro_tarjetas,name='registro_tarjetas')
]