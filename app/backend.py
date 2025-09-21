from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import app.models
import asyncio

from app.routes import health, users, audio

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db import pool

API_VERSION = "/v1"
app = FastAPI()

app.include_router(health.router, prefix=f"{API_VERSION}/health", tags=["Health"])
app.include_router(users.router, prefix=f"{API_VERSION}/users", tags=["Users"])
app.include_router(audio.router, prefix=f"{API_VERSION}/audio", tags=["Audio"] )

# Static directory path
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Page routes
@app.get("/")
def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/login")
def read_login():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/signup")
def read_signup():
    return FileResponse(os.path.join(STATIC_DIR, "signup.html"))

@app.get("/upload")
def read_upload():
    return FileResponse(os.path.join(STATIC_DIR, "upload.html"))
