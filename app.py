from fastapi import FastAPI
import uvicorn
from fastapi import HTTPException

from firebase_adm import init_firebase_admin, verify_token, get_firestore_client
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="Homeschooling API", description="Homeschooling API", version="0.0.1")
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
init_firebase_admin()
db = get_firestore_client()



@app.get("/", tags=["health"])
def health():
    return {
        "service": "Homeschooling API",
        "version": "1.0.0",
        "environment": "DEV",
        "endpoints": {
            "health": "/",
        },
    }
class LoginRequest(BaseModel):
    token: str

@app.post("/login", tags=["login"])
async def login(login_request:LoginRequest):
    id_token = login_request.token
    if not id_token:
        raise HTTPException(status_code=400, detail="token required")
    try:
        decoded_token = verify_token(id_token)
        print(decoded_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    uid = decoded_token["uid"]
    email = decoded_token.get("email")
    name = decoded_token.get("name")
    picture = decoded_token.get("picture")

    try:
        tutor_ref = db.collection("Tutors").document(uid)
        tutor_doc = await tutor_ref.get()

        if not tutor_doc.exists:
            tutor_dict = {
                "id": uid,
                "email": email,
                "name": name,
                "photo_url": picture,
                "created_at": SERVER_TIMESTAMP,
            }
            await tutor_ref.set(tutor_dict)
            print(f"🆕 Authenticated {email}")
        else:
            print(f"✅ User {email} already exists")
        tutor_dict = tutor_doc.to_dict()
        print(f"{tutor_dict=}")
        return {
            "id": tutor_dict.get("id") or uid,
            "email": tutor_dict["email"],
            "name": tutor_dict["name"],
            "photo_url": tutor_dict["photo_url"] 
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in login: {str(e)}")



if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)