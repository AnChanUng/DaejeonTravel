import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from database import engine, Base
from models import Post, Location
from routers import posts, weather, locations, festivals, chat

Base.metadata.create_all(bind=engine)   # 테이블 없으면 생성

os.makedirs("uploads", exist_ok=True)

app = FastAPI(title="LocalHub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 게시글 첨부 이미지 정적 서빙 (http://localhost:8000/uploads/xxx.jpg)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(posts.router)
app.include_router(weather.router)
app.include_router(chat.router)
app.include_router(locations.router)
app.include_router(festivals.router)

@app.get("/")
def root():
    return {"message": "LocalHub API 정상 작동"}