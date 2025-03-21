from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Secret Key for JWT Token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake user database
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": pwd_context.hash("testpassword"),
    }
}


# Verify password function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Login Route
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = fake_users_db.get(username)

    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": username},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
