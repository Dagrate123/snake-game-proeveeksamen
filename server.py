from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import socket 

host = "127.0.0.1"
port = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"connected by{addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    highscore = Column(Integer, default=0)
# lag database tabeller
Base.metadata.create_all(bind=engine)
app = FastAPI()

class UserData(BaseModel):
    username: str
    password: str

class ScoreData(BaseModel):
    username: str
    score: int

@app.post("/register")

def register(user: UserData):
    db = SessionLocal()
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
    new_user = User(
        username=user.username,
        password=user.password,
        highscore=0
    )
    db.add(new_user)
    db.commit()
    return {
        "message": "User created"
    }

@app.post("/login")
def login(user: UserData):
    db = SessionLocal()
    found_user = db.query(User).filter(
        User.username == user.username,
        User.password == user.password
    ).first()

    if not found_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    return {
        "message": "Login successful",
        "highscore": found_user.highscore
    }

@app.post("/save_score")
def save_score(data: ScoreData):
    db = SessionLocal()
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    # lagrer bare hvis du får highscore
    if data.score > user.highscore:
        user.highscore = data.score
        db.commit()

    return {
        "message": "Score saved",
        "highscore": user.highscore
    }

@app.get("/highscore/{username}")
def get_highscore(username: str):
    db = SessionLocal()
    user = db.query(User).filter(
        User.username == username
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "username": user.username,
        "highscore": user.highscore
    }