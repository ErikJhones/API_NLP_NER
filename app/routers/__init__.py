from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {
        "description": "THINA IA Version 0.1",
        "status": "Up and running!",
        "message": "Hello World!!!",
        "docs": "Head over to http://localhost:8000/docs to check the API documentation."
    }
