import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Post
from routers.ws import manager   # 새 글 실시간 알림용

router = APIRouter(prefix="/api/posts", tags=["posts"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB


# --- 요청 형태 정의 ---
class PostCreate(BaseModel):
    category: str
    title: str
    content: str
    password: str
    image: str | None = None
    tags: str | None = None  # "여행,맛집,대전" 형식


class PostUpdate(BaseModel):
    title: str
    content: str
    password: str
    image: str | None = None
    tags: str | None = None


class PasswordCheck(BaseModel):
    password: str


class ReactionRequest(BaseModel):
    action: str  # "like" | "unlike" | "bookmark" | "unbookmark"


def to_summary(p: Post) -> dict:
    return {
        "id": p.id,
        "category": p.category,
        "title": p.title,
        "image": p.image,
        "tags": [t for t in (p.tags or "").split(",") if t],
        "view_count": p.view_count,
        "like_count": p.like_count,
        "bookmark_count": p.bookmark_count,
        "created_at": p.created_at,
    }


def to_detail(p: Post) -> dict:
    return {
        "id": p.id,
        "category": p.category,
        "title": p.title,
        "content": p.content,
        "image": p.image,
        "tags": [t for t in (p.tags or "").split(",") if t],
        "view_count": p.view_count,
        "like_count": p.like_count,
        "bookmark_count": p.bookmark_count,
        "created_at": p.created_at,
        "updated_at": p.updated_at,
    }


# --- 이미지 업로드 ---
@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, "이미지 파일(jpg, png, gif, webp)만 업로드할 수 있습니다")

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(400, "이미지 용량은 5MB를 넘을 수 없습니다")

    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(contents)

    return {"url": f"/uploads/{filename}"}


# --- 목록 조회 (카테고리 필터 + 검색(제목/내용/태그) + 페이지네이션) ---
@router.get("")
def list_posts(
    category: str | None = None,
    keyword: str | None = None,
    tag: str | None = None,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    q = db.query(Post)
    if category:
        q = q.filter(Post.category == category)
    if keyword:
        q = q.filter(
            or_(
                Post.title.contains(keyword),
                Post.content.contains(keyword),
                Post.tags.contains(keyword),
            )
        )
    if tag:
        q = q.filter(Post.tags.contains(tag))

    total = q.count()
    rows = q.order_by(Post.id.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": [to_summary(p) for p in rows],
    }


# --- 여러 게시글 요약 일괄 조회 (북마크 목록 페이지용) ---
# 주의: "/{post_id}"보다 위에 있어야 "batch"가 post_id로 오인되지 않는다.
@router.post("/batch")
def get_posts_batch(ids: list[int], db: Session = Depends(get_db)):
    rows = db.query(Post).filter(Post.id.in_(ids)).all()
    return {"items": [to_summary(p) for p in rows]}


# --- 상세 조회 (비밀번호는 응답에서 제외, 조회수 증가) ---
@router.get("/{post_id}")
def get_post(post_id: int, for_edit: bool = False, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")

    # 수정 화면 진입 시에는 조회수를 올리지 않는다
    if not for_edit:
        post.view_count += 1
        db.commit()
        db.refresh(post)

    return to_detail(post)


# --- 작성 ---
# 저장 후 접속 중인 모든 사용자에게 새 글 알림을 보내야 하므로 async 함수로 정의한다.
@router.post("")
async def create_post(req: PostCreate, db: Session = Depends(get_db)):
    post = Post(**req.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    await manager.broadcast(
        {
            "type": "new_post",
            "post": {
                "id": post.id,
                "title": post.title,
                "category": post.category,
            },
        }
    )

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
    post.image = req.image
    post.tags = req.tags
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


# --- 좋아요 토글 ---
# 로그인 기능이 없어 서버는 카운트만 관리하고, "내가 눌렀는지"는 프론트에서
# localStorage로 기억한다 (기기별로 유지됨).
@router.post("/{post_id}/like")
def toggle_like(post_id: int, req: ReactionRequest, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")

    if req.action == "like":
        post.like_count += 1
    elif req.action == "unlike":
        post.like_count = max(0, post.like_count - 1)
    else:
        raise HTTPException(400, "action은 like 또는 unlike여야 합니다")

    db.commit()
    return {"like_count": post.like_count}


# --- 북마크 토글 ---
@router.post("/{post_id}/bookmark")
def toggle_bookmark(post_id: int, req: ReactionRequest, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")

    if req.action == "bookmark":
        post.bookmark_count += 1
    elif req.action == "unbookmark":
        post.bookmark_count = max(0, post.bookmark_count - 1)
    else:
        raise HTTPException(400, "action은 bookmark 또는 unbookmark여야 합니다")

    db.commit()
    return {"bookmark_count": post.bookmark_count}