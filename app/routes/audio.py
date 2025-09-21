import os
from fastapi import APIRouter, Form, Depends, File, UploadFile, HTTPException
from app.db import pool
import psycopg
from psycopg.rows import dict_row
import shutil
import time

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
def get_all_audios():
    try:
        with psycopg.connect(
            host="localhost", dbname="soundmap-db", user="postgres", password="postgres", row_factory=dict_row
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, location, description, tags, date, time_of_day, file_path, file_type, uploaded_at
                    FROM audios
                    ORDER BY date DESC
                    """,
                )
                results = cur.fetchall()
                if not results:
                    return {"audios": []}
                return {"audios": results}
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{location}")
def get_audios(location: str):
    try:
        with psycopg.connect(
            host="localhost", dbname="soundmap-db", user="postgres", password="postgres", row_factory=dict_row
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT title, location, description, tags, date, time_of_day, file_path
                    FROM audios
                    WHERE location = %s
                    ORDER BY date DESC
                    """,
                    (location,)
                )
                results = cur.fetchall()
                if not results:
                    return {"audios": []}
                return {"audios": results}
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_audio(
    title: str = Form(...),
    place: str = Form(...),
    date: str = Form(...),
    timeOfDay: str = Form(...),
    audioFile: UploadFile = File(...),
    tags: str = Form(...),
    description: str = Form(None),
):
    if not audioFile.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio type")

    try:
        # Generate unique filename
        timestamp = int(time.time())
        unique_filename = f"{timestamp}_{audioFile.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        file_name = os.path.join(UPLOAD_DIR, audioFile.filename)


        _, file_type = os.path.splitext(audioFile.filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audioFile.file, buffer)

        # Insert into DB
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO audios 
                       (title, location, description, tags, date, time_of_day, file_path, file_type)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                       RETURNING id""",
                    (title, place, description, tags, date, timeOfDay, file_path, file_type)
                )
                audio_id = cur.fetchone()[0]
                conn.commit()

        return {"status": "success", "audio_id": audio_id}

    except Exception as e:
        print("Upload error:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{audio_id}")
async def delete_audio(audio_id: int):
    """
    Deletes an audio by ID: removes the DB record and deletes the file from disk.
    """
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            # Fetch the file path first
            await cur.execute("SELECT file_path FROM audios WHERE id = %s", (audio_id,))
            result = await cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Audio not found")
            
            file_path = result[0]

            # Delete the database record
            await cur.execute("DELETE FROM audios WHERE id = %s", (audio_id,))

    # Delete the file if it exists
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    return {"message": "Audio deleted successfully"}