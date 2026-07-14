from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Post

router = APIRouter(prefix="/api/posts", tags=["posts"])

# --- 요청 형태 정의 ---
class PostCreate(BaseModel):
    category: str
    title: str
    content: str
    password: str

class PostUpdate(BaseModel):
    title: str
    content: str
    password: str

class PasswordCheck(BaseModel):
    password: str

# --- 목록 조회 (카테고리 필터 + 검색 + 페이지네이션) ---
@router.get("")
def list_posts(category: str | None = None, keyword: str | None = None,
               page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    q = db.query(Post)
    if category:
        q = q.filter(Post.category == category)
    if keyword:
        q = q.filter(Post.title.contains(keyword))
    total = q.count()
    rows = q.order_by(Post.id.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": [
            {"id": p.id, "category": p.category, "title": p.title,
             "created_at": p.created_at}
            for p in rows
        ],
    }

# --- 상세 조회 (비밀번호는 응답에서 제외) ---
@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")
    return {
        "id": post.id, "category": post.category, "title": post.title,
        "content": post.content, "created_at": post.created_at,
        "updated_at": post.updated_at,
    }

# --- 작성 ---
@router.post("")
def create_post(req: PostCreate, db: Session = Depends(get_db)):
    post = Post(**req.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id, "message": "작성 완료"}

# --- 수정 (비밀번호 일치 시만) ---
@router.put("/{post_id}")
def update_post(post_id: int, req: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")
    if post.password != req.password:
        raise HTTPException(403, "비밀번호가 일치하지 않습니다")
    post.title = req.title
    post.content = req.content
    db.commit()
    return {"id": post.id, "message": "수정 완료"}

# --- 삭제 (비밀번호 일치 시만) ---
@router.delete("/{post_id}")
def delete_post(post_id: int, req: PasswordCheck, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")
    if post.password != req.password:
        raise HTTPException(403, "비밀번호가 일치하지 않습니다")
    db.delete(post)
    db.commit()
    return {"message": "삭제 완료"}