# app/firebase_admin.py

import firebase_admin
from firebase_admin import credentials, auth
import os
import json
from dotenv import load_dotenv
load_dotenv()
# Inicializar Firebase Admin solo una vez
if not firebase_admin._apps:
    firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
    if firebase_creds:
        cred_dict = json.loads(firebase_creds)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

def verify_token(id_token: str):
    """
    Verifica un Firebase ID Token y devuelve la información del usuario.
    Lanza un error si es inválido o expirado.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token  # contiene: uid, email, name, etc.
    except Exception as e:
        raise ValueError(f"Token inválido: {e}")
