from django.urls import path
from . import views

urlpatterns = [
    path('', views.logout,name='bases'),
    path('cambiar_locacion/',views.cambiar_locacion,name='cambiar_locacion')
]