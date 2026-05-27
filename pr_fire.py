#Funciones add 
from firebase_admin import db
import firebase_service as sv
import firebase_config

print(sv.obtener_pedido_por_folio('10415'))