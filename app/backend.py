from fastapi import FastAPI

app = FastAPI()

API_VERSION = "/v1"

@app.get("/")
def read_index():
    return{"app": "running"}