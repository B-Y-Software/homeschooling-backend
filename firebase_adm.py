# app/firebase_admin.py

import firebase_admin
from firebase_admin import auth
import os
import json
from google.oauth2 import service_account
from google.cloud.firestore_v1 import AsyncClient
from dotenv import load_dotenv
load_dotenv()

# Inicializar Firebase Admin solo una vez

def get_credentials():
    """
    Devuelve las credenciales de Firebase Admin.
    """
    firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
    if firebase_creds:
        cred_dict = json.loads(firebase_creds)
        credentials = service_account.Credentials.from_service_account_info(cred_dict)
        return credentials
    return None
def init_firebase_admin():
    """
    Inicializa la aplicación Firebase Admin si no está ya inicializada.
    y devuelve una instancia del cliente Firestore.
    """
    if not firebase_admin._apps:
        credentials = get_credentials()
        if credentials:
            firebase_admin.initialize_app(credentials)
            return AsyncClient(credentials=credentials, project=credentials.project_id)
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

# def get_firestore_client() -> AsyncClient:
#     """
#     Devuelve una instancia del cliente Firestore.
#     """
#     credentials = get_credentials()
    
#     return AsyncClient(credentials=credentials, project=credentials.project_id)



