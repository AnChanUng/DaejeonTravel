# import_data.py — 딱 한 번 실행하는 스크립트
import json
from pathlib import Path
from database import engine, SessionLocal, Base
from models import Location

Base.metadata.create_all(bind=engine)   # 테이블 생성

def to_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None

db = SessionLocal()
data_dir = Path("data")

for json_file in data_dir.glob("*.json"):
    with open(json_file, encoding="utf-8") as f:
        payload = json.load(f)

    content_type = payload.get("contentType", json_file.stem)  # "관광지" 등
    items = payload.get("items", [])

    for item in items:
        # 중복 방지: 이미 있으면 skip
        exists = db.query(Location).filter(
            Location.content_id == item["contentid"]
        ).first()
        if exists:
            continue

        db.add(Location(
            content_id=item["contentid"],
            content_type=content_type,
            title=item.get("title", ""),
            addr=(item.get("addr1", "") + " " + item.get("addr2", "")).strip(),
            lat=to_float(item.get("mapy")),   # y = 위도
            lng=to_float(item.get("mapx")),   # x = 경도
            image=item.get("firstimage", ""),
            tel=item.get("tel", ""),
        ))
    print(f"{json_file.name}: {len(items)}건 처리")

db.commit()
db.close()
print("적재 완료")