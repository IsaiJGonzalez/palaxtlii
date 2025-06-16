from django.urls import path
from . import views


urlpatterns = [
    path('',views.codigos,name='codigos'),
    path('agregar_cat/',views.agregar_cat,name='')
]