from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Location

router = APIRouter(prefix="/api/locations", tags=["locations"])

# 지역 필터 → 주소 접두어 매핑
REGION_PREFIX = {
    "대전": "대전",
    "세종": "세종",
    "충남": "충청남도",
    "충북": "충청북도",
}


def to_dict(loc: Location) -> dict:
    return {
        "id": loc.id,
        "content_id": loc.content_id,
        "content_type": loc.content_type,
        "title": loc.title,
        "addr": loc.addr,
        "lat": loc.lat,
        "lng": loc.lng,
        "image": loc.image,
        "tel": loc.tel,
    }


# --- 목록 조회 (타입 필수 + 지역/검색 필터 + 페이지네이션) ---
@router.get("")
def list_locations(
    type: str,
    region: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    size: int = 12,
    db: Session = Depends(get_db),
):
    q = db.query(Location).filter(Location.content_type == type)

    if region and region in REGION_PREFIX:
        q = q.filter(Location.addr.startswith(REGION_PREFIX[region]))

    if keyword:
        q = q.filter(Location.title.contains(keyword))

    total = q.count()

    # 이미지 있는 장소를 먼저 보여줘서 목록이 풍성해 보이게
    rows = (
        q.order_by((Location.image == "").asc(), Location.title.asc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": [to_dict(r) for r in rows],
    }


# --- 상세 조회 ---
@router.get("/{content_id}")
def get_location(content_id: str, db: Session = Depends(get_db)):
    loc = (
        db.query(Location)
        .filter(Location.content_id == content_id)
        .first()
    )
    if not loc:
        raise HTTPException(404, "장소를 찾을 수 없습니다")
    return to_dict(loc)