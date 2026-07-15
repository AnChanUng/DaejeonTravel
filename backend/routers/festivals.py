import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter(prefix="/api/festivals", tags=["festivals"])

SOURCE = Path("data/대전_충청권/대전_충청권_축제공연행사.json")
DATES = Path("data/festival_dates.json")


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


def to_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def load_festivals():
    """축제 원본 JSON + 날짜 매핑 파일 병합.
    데이터가 26건뿐이라 DB 없이 요청 시 파일에서 읽는다."""
    with open(SOURCE, encoding="utf-8") as f:
        payload = json.load(f)

    dates = {}
    if DATES.exists():
        with open(DATES, encoding="utf-8") as f:
            dates = json.load(f)

    events, undated = [], []
    for item in payload.get("items", []):
        cid = item["contentid"]
        addr = (item.get("addr1", "") + " " + item.get("addr2", "")).strip()
        d = dates.get(cid, {})
        festival = {
            "content_id": cid,
            "title": item.get("title", ""),
            "addr": addr,
            "region": region_of(addr),
            "image": item.get("firstimage", ""),
            "tel": item.get("tel", ""),
            "lat": to_float(item.get("mapy")),
            "lng": to_float(item.get("mapx")),
            "start": d.get("start", ""),
            "end": d.get("end", "") or d.get("start", ""),
        }
        if festival["start"]:
            events.append(festival)
        else:
            undated.append(festival)

    return events, undated


@router.get("")
def list_festivals():
    events, undated = load_festivals()
    return {"events": events, "undated": undated}