from django.urls import path
from . import views

urlpatterns = [

    # Página principal
    path('', views.editar_pedido_page, name='editar_pedido_page'),

    # Obtener folios activos
    path('api/folios/', views.api_folios, name='api_folios'),

    # Obtener pedido por ID
    path('api/pedido/<str:pedido_id>/', views.api_pedido, name='api_pedido'),

    # Editar pedido
    path('api/editar/<str:pedido_id>/', views.api_editar_pedido, name='api_editar_pedido'),

]
