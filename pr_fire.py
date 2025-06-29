#Funciones add 
from firebase_admin import db
import firebase_service as sv
import firebase_config

no_emp = 908298
caja_activa = sv.consultar_caja_activa(no_emp)

if caja_activa :
    print(1)
