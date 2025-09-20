from fastapi import APIRouter
from app.db import engine
from sqlalchemy import text

router = APIRouter()

@router.get("/")
def health():
    return {"status": "up"}

@router.get("/db")
def db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": f"connection failed: {e}"}