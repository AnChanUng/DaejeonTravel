from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import Post

# 장소 데이터는 DB가 아니라 JSON 파일에서 읽으므로
# locations 라우터의 로더를 그대로 재사용한다.
from routers.locations import (
    LOCATION_FILES,
    load_locations_by_type,
)

router = APIRouter(
    prefix="/api/stats",
    tags=["stats"],
)


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
    # --- 게시글 통계 (DB) ---
    total_posts = db.query(func.count(Post.id)).scalar() or 0

    total_views = db.query(
        func.coalesce(func.sum(Post.view_count), 0)
    ).scalar()

    total_likes = db.query(
        func.coalesce(func.sum(Post.like_count), 0)
    ).scalar()

    by_category = [
        {
            "category": category,
            "count": count,
        }
        for category, count in (
            db.query(Post.category, func.count(Post.id))
            .group_by(Post.category)
            .all()
        )
    ]

    top_viewed = [
        {
            "id": post.id,
            "title": post.title,
            "view_count": post.view_count,
            "like_count": post.like_count,
        }
        for post in (
            db.query(Post)
            .order_by(
                Post.view_count.desc(),
                Post.id.desc(),
            )
            .limit(5)
            .all()
        )
    ]

    # --- 장소 통계 (JSON) ---
    region_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    total_locations = 0

    for location_type in LOCATION_FILES:
        locations = load_locations_by_type(location_type)

        total_locations += len(locations)
        type_counts[location_type] = len(locations)

        for location in locations:
            region = region_of(location["addr"])
            region_counts[region] = region_counts.get(region, 0) + 1

    by_region = [
        {
            "region": region,
            "count": count,
        }
        for region, count in sorted(
            region_counts.items(),
            key=lambda pair: -pair[1],
        )
    ]

    by_type = [
        {
            "type": location_type,
            "count": count,
        }
        for location_type, count in sorted(
            type_counts.items(),
            key=lambda pair: -pair[1],
        )
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