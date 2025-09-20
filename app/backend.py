from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

from app.routes import health

API_VERSION = "/v1"
app = FastAPI()

app.include_router(health.router, prefix=f"{API_VERSION}/health", tags=["Health"])


@app.get("/")
def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "main.html"))
