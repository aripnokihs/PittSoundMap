import os
from fastapi import APIRouter, Form, Depends
from app.db import pool
import psycopg
from psycopg.rows import dict_row

router = APIRouter()

conninfo = (
    f"host={os.getenv('DB_HOST', 'localhost')} "
    f"port={os.getenv('DB_PORT', 5432)} "
    f"dbname={os.getenv('DB_NAME', 'postgres')} "
    f"user={os.getenv('DB_USER', 'postgres')} "
    f"password={os.getenv('DB_PASSWORD', 'postgres')}"
)

@router.get("/")
def root():
    return {"status": "up"}

@router.post("/add")
async def add_user(username: str = Form(...)):
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING user_id",
                    (username, "hashedpassword")
                )
                user_id = cur.fetchone()[0]
                conn.commit()
        return {"status": "success", "user_id": user_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}