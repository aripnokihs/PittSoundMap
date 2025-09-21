import os
from fastapi import APIRouter, Form, Depends, File, UploadFile, HTTPException
from app.db import pool
import psycopg
from psycopg.rows import dict_row
import shutil

router = APIRouter()

conninfo = (
    f"host={os.getenv('DB_HOST', 'localhost')} "
    f"port={os.getenv('DB_PORT', 5432)} "
    f"dbname={os.getenv('DB_NAME', 'postgres')} "
    f"user={os.getenv('DB_USER', 'postgres')} "
    f"password={os.getenv('DB_PASSWORD', 'postgres')}"
)

UPLOAD_DIR = "audios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    file_path = os.path.join(UPLOAD_DIR, audioFile.filename)
    
    # File type / extension
    _, file_type = os.path.splitext(audioFile.filename)
    
    # Save the file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audioFile.file, buffer)
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO audios (title, location, description, tags, date, time_of_day, file_path, file_type)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id """,
                    (title, 
                     place,
                     description,
                     tags,
                     date,
                     timeOfDay,
                     file_path,
                     file_type
                     )
                )
                user_id = cur.fetchone()[0]
                conn.commit()
        return {"status": "success", "user_id": user_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}