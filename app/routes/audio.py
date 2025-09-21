import os
from fastapi import APIRouter, Form, Depends, File, UploadFile, HTTPException
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

@router.post("/upload")
async def upload_audio(
    title: str = Form(...),
    place: str = Form(...),
    date: str = Form(...),  # or `date: date = Form(...)` if you want auto-parsing
    timeOfDay: str = Form(...),
    audioFile: UploadFile = File(...),
    tags: str = Form(...),
    description: str = Form(None),
):
    
    if not audioFile.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio type")
    
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO audios (user_id, title, location, description, tags, date, time_of_day, file_path, file_type, uploaded_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id """,
                    (username, 
                     password
                     )
                )
                user_id = cur.fetchone()[0]
                conn.commit()
        return {"status": "success", "user_id": user_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}