from . import views
from django.urls import path

urlpatterns = [
    path('',views.apertura_caja,name='apertura_caja')
]
