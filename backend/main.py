from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base
from models import Post, Location
from routers import posts, weather, chat

Base.metadata.create_all(bind=engine)   # posts 테이블 없으면 생성

app = FastAPI(title="LocalHub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(weather.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "LocalHub API 정상 작동"}