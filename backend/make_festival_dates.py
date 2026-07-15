# make_festival_dates.py — 축제 날짜 매핑 템플릿 생성 (한 번만 실행)
#
# 실행: python make_festival_dates.py
# 결과: data/festival_dates.json 생성
#
# 생성된 파일의 start/end를 팀원들이 채우면 캘린더에 표시된다.
# 날짜 형식: "YYYY-MM-DD" / 모르는 축제는 빈 문자열로 두면 '일정 확인 중' 목록에 표시됨.
import json
from pathlib import Path

SOURCE = Path("data/대전_충청권/대전_충청권_축제공연행사.json")
TARGET = Path("data/festival_dates.json")

with open(SOURCE, encoding="utf-8") as f:
    payload = json.load(f)

# 이미 파일이 있으면 기존 입력값 보존
existing = {}
if TARGET.exists():
    with open(TARGET, encoding="utf-8") as f:
        existing = json.load(f)

result = {}
for item in payload.get("items", []):
    cid = item["contentid"]
    prev = existing.get(cid, {})
    result[cid] = {
        "_title": item.get("title", ""),   # 참고용 (백엔드는 무시)
        "start": prev.get("start", ""),
        "end": prev.get("end", ""),
    }

with open(TARGET, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"{TARGET} 생성 완료 — {len(result)}건")
print("start / end 에 YYYY-MM-DD 형식으로 날짜를 채워주세요.")