from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Post, Location

router = APIRouter(prefix="/api/stats", tags=["stats"])


def region_of(addr: str) -> str:
    if addr.startswith("대전"):
        return "대전"
    if addr.startswith("세종"):
        return "세종"
    if addr.startswith("충청남도"):
        return "충남"
    if addr.startswith("충청북도"):
        return "충북"
    return "기타"


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    # --- 게시글 통계 ---
    total_posts = db.query(func.count(Post.id)).scalar() or 0
    total_views = db.query(func.coalesce(func.sum(Post.view_count), 0)).scalar()
    total_likes = db.query(func.coalesce(func.sum(Post.like_count), 0)).scalar()

    by_category = [
        {"category": c, "count": n}
        for c, n in (
            db.query(Post.category, func.count(Post.id))
            .group_by(Post.category)
            .all()
        )
    ]

    top_viewed = [
        {
            "id": p.id,
            "title": p.title,
            "view_count": p.view_count,
            "like_count": p.like_count,
        }
        for p in (
            db.query(Post)
            .order_by(Post.view_count.desc(), Post.id.desc())
            .limit(5)
            .all()
        )
    ]

    # --- 장소 통계 (전체 1,365건 정도라 파이썬에서 집계해도 충분) ---
    locations = db.query(Location.addr, Location.content_type).all()
    total_locations = len(locations)

    region_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for addr, ctype in locations:
        r = region_of(addr or "")
        region_counts[r] = region_counts.get(r, 0) + 1
        type_counts[ctype] = type_counts.get(ctype, 0) + 1

    by_region = [
        {"region": r, "count": n}
        for r, n in sorted(region_counts.items(), key=lambda x: -x[1])
    ]
    by_type = [
        {"type": t, "count": n}
        for t, n in sorted(type_counts.items(), key=lambda x: -x[1])
    ]

    return {
        "posts": {
            "total": total_posts,
            "total_views": total_views,
            "total_likes": total_likes,
            "by_category": by_category,
            "top_viewed": top_viewed,
        },
        "locations": {
            "total": total_locations,
            "by_region": by_region,
            "by_type": by_type,
        },
    }