from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    category = Column(String, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    password = Column(String, nullable=False)
    image = Column(String, nullable=True)          # 대표 이미지 URL (/uploads/xxx.jpg)
    tags = Column(String, nullable=True)            # 콤마(,)로 구분된 태그 문자열
    view_count = Column(Integer, default=0, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    bookmark_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)