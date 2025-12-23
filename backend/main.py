from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import User
from schemas import UserCreate
from security.hash import hash_password
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
from security.hash import verify_password
from security.jwt import create_access_token
from fastapi.middleware.cors import CORSMiddleware

from parser import parse_log
from features import extract_features
from detector import detect_anomalies, add_explanations

app = FastAPI()

# ⭐ CORS 一定要在「所有 router 之前」
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created"}

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Try again later."}
    )

@app.post("/login")
@limiter.limit("5/minute")  # 每分鐘最多 5 次
def login(user: UserCreate, db: Session = Depends(get_db), request: Request = None):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/analyze/logs")
def analyze_logs():
    df = parse_log()
    df = extract_features(df)
    df = detect_anomalies(df)
    df = add_explanations(df)
    result = df.to_dict(orient="records")
    return {"logs": result}