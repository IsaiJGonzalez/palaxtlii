from django.urls import path
from . import views

urlpatterns = [
    path('',views.main_gerencial, name='menu_gerencial')
]