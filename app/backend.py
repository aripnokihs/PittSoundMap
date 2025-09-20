from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routes import health

app = FastAPI()
app.include_router(health.router)


API_VERSION = "/v1"

@app.get("/")
def read_index():
    return FileResponse("app/static/main.html")
