import os
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
import psycopg
from psycopg.rows import dict_row
from passlib.hash import bcrypt
from fastapi import APIRouter, Form, Response, Request
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from itsdangerous import URLSafeSerializer

router = APIRouter()

# ✅ Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Secret key for cookie signing
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
serializer = URLSafeSerializer(SECRET_KEY, salt="session")

# Connection info
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

# ✅ Signup (hash password before saving)
@router.post("/add")
async def add_user(username: str = Form(...), password: str = Form(...)):
    try:
        hashed_pw = bcrypt.hash(password)  # hash the password

        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING user_id",
                    (username, hashed_pw)
                )
                user_id = cur.fetchone()[0]
                conn.commit()

        return RedirectResponse(url="/static/index.html", status_code=303)
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ✅ Login (verify password against hash)
@router.post("/get")
async def get_user(username: str = Form(...), password: str = Form(...)):
    try:
        with psycopg.connect(conninfo, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT username, password_hash FROM users WHERE username = %s",
                    (username,)
                )
                user = cur.fetchone()

        if not user:
            return {"status": "error", "message": "User not found"}

        # Verify password
        if not bcrypt.verify(password, user["password_hash"]):
            return {"status": "error", "message": "Invalid password"}

        # Login success → redirect to homepage
        return RedirectResponse(url=f"/?user={username}", status_code=303)

    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/login")
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    response: Response = None
):
    try:
        with psycopg.connect(conninfo, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, password_hash FROM users WHERE username = %s", (username,))
                user = cur.fetchone()

        if not user or not pwd_context.verify(password, user["password_hash"]):
            return JSONResponse({"status": "error", "message": "Invalid credentials"}, status_code=401)

        # Create signed cookie
        session_token = serializer.dumps({"username": username})
        response.set_cookie(
            key="session",
            value=session_token,
            httponly=True,  # protects from JavaScript access
            samesite="lax",
        )

        return {"status": "success", "user": username}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/session")
async def get_session(request: Request):
    """Check session cookie and return current user if valid"""
    token = request.cookies.get("session")
    if not token:
        return {"user": None}

    try:
        data = serializer.loads(token)
        return {"user": data["username"]}
    except Exception:
        return {"user": None}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"status": "success", "message": "Logged out"}