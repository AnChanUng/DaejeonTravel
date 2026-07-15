from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from database import Base
 
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    content_id = Column(String, unique=True, index=True)
    content_type = Column(String, index=True)
    title = Column(String, index=True)
    addr = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    image = Column(String)
    tel = Column(String)
 
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