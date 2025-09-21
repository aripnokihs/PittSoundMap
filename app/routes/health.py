from fastapi import APIRouter
from app.db import pool
import psycopg
from psycopg.rows import dict_row
from sqlalchemy import text

router = APIRouter()

@router.get("/")
def health():
    return {"status": "up"}

@router.get("/db")
async def db_connection():
    try:
        async with pool.connection() as conn:   # acquire a connection
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("SELECT 1")
                await cur.fetchone()
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": str(e)}