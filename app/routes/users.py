import os
from fastapi import APIRouter, Form, Depends
from fastapi.responses import FileResponse, RedirectResponse
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
async def add_user(username: str = Form(...), password: str = Form(...)):
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING user_id",
                    (username, password)
                )
                user_id = cur.fetchone()[0]
                conn.commit()
        return RedirectResponse(url="/static/index.html", status_code=303)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@router.post("/get")
async def get_user(username: str = Form(...), password: str = Form(...)):
    try:
        with psycopg.connect(conninfo, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT username, password_hash FROM users WHERE username = %s AND password_hash = %s",
                    (username,password)
                )
                user = cur.fetchone()
        if not user:
            return {"status": "error", "message": "User not found"}
        return {"status": "success", "user": user}
    except Exception as e:
        return {"status": "error", "message": str(e)}