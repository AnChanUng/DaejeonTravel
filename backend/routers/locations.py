import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(
    prefix="/api/locations",
    tags=["locations"],
)

# backend 폴더
BACKEND_DIR = Path(__file__).resolve().parent.parent

# backend/data/대전_충청권
DATA_DIR = BACKEND_DIR / "data" / "대전_충청권"

# 화면의 장소 유형과 JSON 파일 연결
LOCATION_FILES = {
    "관광지": DATA_DIR / "대전_충청권_관광지.json",
    "음식점": DATA_DIR / "대전_충청권_음식점.json",
    "숙박": DATA_DIR / "대전_충청권_숙박.json",
}

# 관광공사 contenttypeid
CONTENT_TYPE_NAME = {
    "12": "관광지",
    "32": "숙박",
    "39": "음식점",
}

# 지역 필터
REGION_PREFIX = {
    "대전": "대전",
    "세종": "세종",
    "충남": "충청남도",
    "충북": "충청북도",
}


def extract_items(data: Any) -> list[dict]:
    """
    JSON 구조가 배열이거나 items/item 형태여도
    장소 목록을 추출할 수 있도록 처리합니다.
    """
    if isinstance(data, list):
        return [
            item
            for item in data
            if isinstance(item, dict)
        ]

    if not isinstance(data, dict):
        return []

    # {"items": [...]}
    items = data.get("items")

    if isinstance(items, list):
        return [
            item
            for item in items
            if isinstance(item, dict)
        ]

    # {"items": {"item": [...]}}
    if isinstance(items, dict):
        item_list = items.get("item")

        if isinstance(item_list, list):
            return [
                item
                for item in item_list
                if isinstance(item, dict)
            ]

        if isinstance(item_list, dict):
            return [item_list]

    # 관광공사 API 응답 구조
    # {"response": {"body": {"items": {"item": [...]}}}}
    response = data.get("response")

    if isinstance(response, dict):
        body = response.get("body", {})

        if isinstance(body, dict):
            return extract_items(body)

    # {"data": [...]}, {"results": [...]} 형태 대응
    for key in ("data", "results"):
        value = data.get(key)

        if isinstance(value, list):
            return [
                item
                for item in value
                if isinstance(item, dict)
            ]

        if isinstance(value, dict):
            extracted = extract_items(value)

            if extracted:
                return extracted

    return []


def read_json_file(file_path: Path) -> list[dict]:
    if not file_path.exists():
        print(f"JSON 파일을 찾을 수 없습니다: {file_path}")
        return []

    try:
        # UTF-8 BOM이 포함된 파일도 읽을 수 있도록 utf-8-sig 사용
        with file_path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = json.load(file)

        return extract_items(data)

    except json.JSONDecodeError as error:
        print(f"JSON 형식 오류: {file_path}")
        print(error)
        return []

    except OSError as error:
        print(f"JSON 파일 읽기 실패: {file_path}")
        print(error)
        return []


def normalize_location(
    item: dict,
    location_type: str | None = None,
) -> dict:
    """
    JSON 필드를 프론트엔드에서 사용하는 필드명으로 변환합니다.
    """
    content_type = str(
        item.get("contenttypeid")
        or item.get("content_type")
        or ""
    )

    resolved_type = (
        location_type
        or CONTENT_TYPE_NAME.get(content_type)
        or content_type
    )

    addr1 = str(item.get("addr1") or "").strip()
    addr2 = str(item.get("addr2") or "").strip()

    address = " ".join(
        value
        for value in (addr1, addr2)
        if value
    )

    return {
        # 기존 프론트 코드 호환용
        "id": str(
            item.get("contentid")
            or item.get("content_id")
            or item.get("id")
            or ""
        ),
        "content_id": str(
            item.get("contentid")
            or item.get("content_id")
            or item.get("id")
            or ""
        ),
        "content_type": resolved_type,
        "content_type_id": content_type,

        "title": str(
            item.get("title")
            or item.get("name")
            or ""
        ).strip(),

        "addr": address,
        "addr1": addr1,
        "addr2": addr2,

        "lat": item.get("mapy") or item.get("lat"),
        "lng": item.get("mapx") or item.get("lng"),

        "image": (
            item.get("firstimage")
            or item.get("image")
            or ""
        ),
        "image2": (
            item.get("firstimage2")
            or item.get("image2")
            or ""
        ),

        "tel": item.get("tel") or "",
        "zipcode": item.get("zipcode") or "",
    }


def load_locations_by_type(
    location_type: str,
) -> list[dict]:
    file_path = LOCATION_FILES.get(location_type)

    if not file_path:
        return []

    raw_items = read_json_file(file_path)

    return [
        normalize_location(
            item,
            location_type,
        )
        for item in raw_items
    ]


def load_all_searchable_locations() -> list[dict]:
    locations: list[dict] = []

    for location_type in LOCATION_FILES:
        locations.extend(
            load_locations_by_type(location_type)
        )

    return locations


# 목록 조회
@router.get("")
def list_locations(
    type: str,
    region: str | None = None,
    keyword: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=12, ge=1, le=100),
):
    if type not in LOCATION_FILES:
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 장소 유형입니다.",
        )

    locations = load_locations_by_type(type)

    if region and region in REGION_PREFIX:
        prefix = REGION_PREFIX[region]

        locations = [
            location
            for location in locations
            if location["addr"].startswith(prefix)
        ]

    if keyword:
        cleaned_keyword = keyword.strip()

        if cleaned_keyword:
            locations = [
                location
                for location in locations
                if cleaned_keyword in location["title"]
            ]

    # 이미지가 있는 장소 우선, 이후 이름순 정렬
    locations.sort(
        key=lambda location: (
            not bool(location["image"]),
            location["title"],
        )
    )

    total = len(locations)
    start = (page - 1) * size
    end = start + size

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": locations[start:end],
    }


# 검색어 자동완성
@router.get("/suggestions")
def suggest_locations(
    keyword: str = Query(min_length=1),
    limit: int = Query(default=5, ge=1, le=10),
):
    cleaned_keyword = keyword.strip()

    if not cleaned_keyword:
        return {
            "items": [],
        }

    locations = load_all_searchable_locations()

    matched_locations = [
        location
        for location in locations
        if cleaned_keyword in location["title"]
    ]

    # 정확히 일치하는 장소를 먼저 표시
    matched_locations.sort(
        key=lambda location: (
            location["title"] != cleaned_keyword,
            location["title"],
        )
    )

    return {
        "items": matched_locations[:limit],
    }


# 장소명 정확히 일치 검색
@router.get("/exact")
def find_exact_location(
    keyword: str = Query(min_length=1),
):
    cleaned_keyword = keyword.strip()

    locations = load_all_searchable_locations()

    location = next(
        (
            item
            for item in locations
            if item["title"] == cleaned_keyword
        ),
        None,
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="검색 결과가 없습니다.",
        )

    return location


# 장소 상세 조회
# suggestions와 exact보다 반드시 아래에 있어야 합니다.
@router.get("/{content_id}")
def get_location(content_id: str):
    locations = load_all_searchable_locations()

    location = next(
        (
            item
            for item in locations
            if item["content_id"] == content_id
        ),
        None,
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="장소를 찾을 수 없습니다.",
        )

    return location