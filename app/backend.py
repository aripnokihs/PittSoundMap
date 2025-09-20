from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import app.models
import asyncio

from app.routes import health, users

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db import pool

API_VERSION = "/v1"
app = FastAPI()

app.include_router(health.router, prefix=f"{API_VERSION}/health", tags=["Health"])
app.include_router(users.router, prefix=f"{API_VERSION}/users", tags=["Users"])


@app.get("/")
def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "test.html"))
