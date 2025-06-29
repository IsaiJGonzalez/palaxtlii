import firebase_admin
from firebase_admin import credentials, firestore, db

# Ruta al archivo JSON con credenciales
keys = credentials.Certificate("C:/Users/isaij/Desktop/keys.json")
firebase_admin.initialize_app(keys,{
    "databaseURL": "https://palaxtlipr-default-rtdb.firebaseio.com"
})

fr_db = db.reference('/')