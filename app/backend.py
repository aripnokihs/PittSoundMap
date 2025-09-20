from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

API_VERSION = "/v1"

@app.get("/")
def read_index():
    return FileResponse("app/static/main.html")

