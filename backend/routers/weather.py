from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/api/weather", tags=["weather"])

# 대전/충청 권역 대표 지점 (DB locations의 lat/lng를 써도 되지만,
# 날씨는 도시 단위면 충분해서 대표 좌표로 고정)
REGIONS = {
    "대전": {"lat": 36.3504, "lng": 127.3845},
    "청주": {"lat": 36.6424, "lng": 127.4890},
    "천안": {"lat": 36.8151, "lng": 127.1139},
    "세종": {"lat": 36.4800, "lng": 127.2890},
}

# Open-Meteo weathercode → 한글 설명 매핑 (주요 코드만)
WEATHER_DESC = {
    0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
    45: "안개", 48: "짙은 안개",
    51: "가랑비", 53: "이슬비", 55: "강한 이슬비",
    61: "약한 비", 63: "비", 65: "강한 비",
    71: "약한 눈", 73: "눈", 75: "강한 눈",
    80: "소나기", 81: "강한 소나기", 82: "폭우",
    95: "뇌우", 96: "우박 동반 뇌우", 99: "강한 우박 뇌우",
}

def judge_travel(temp: float, code: int, wind: float) -> dict:
    """여행 적합 여부 판단 — RFP 요구의 핵심 로직"""
    score = 100
    reasons = []

    # 강수/악천후 감점
    if code >= 95:
        score -= 60; reasons.append("뇌우")
    elif code >= 80:
        score -= 40; reasons.append("소나기")
    elif code >= 71:
        score -= 30; reasons.append("눈")
    elif code >= 61:
        score -= 35; reasons.append("비")
    elif code >= 51:
        score -= 15; reasons.append("이슬비")
    elif code >= 45:
        score -= 10; reasons.append("안개")

    # 기온 감점
    if temp >= 33:
        score -= 30; reasons.append("폭염")
    elif temp >= 30:
        score -= 15; reasons.append("더움")
    elif temp <= -10:
        score -= 30; reasons.append("한파")
    elif temp <= 0:
        score -= 15; reasons.append("추움")

    # 강풍 감점
    if wind >= 14:
        score -= 20; reasons.append("강풍")
    elif wind >= 9:
        score -= 10; reasons.append("바람 강함")

    if score >= 80:
        return {"grade": "좋음", "emoji": "😊", "comment": "여행하기 딱 좋은 날씨예요"}
    elif score >= 55:
        return {"grade": "보통", "emoji": "🙂", "comment": f"무난해요 ({', '.join(reasons)})"}
    else:
        return {"grade": "나쁨", "emoji": "😷", "comment": f"실내 위주 일정을 추천해요 ({', '.join(reasons)})"}

@router.get("")
async def get_weather():
    results = []
    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, coord in REGIONS.items():
            try:
                res = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": coord["lat"],
                        "longitude": coord["lng"],
                        "current": "temperature_2m,weathercode,windspeed_10m",
                        "timezone": "Asia/Seoul",
                    },
                )
                cur = res.json()["current"]
                temp = cur["temperature_2m"]
                code = cur["weathercode"]
                wind = cur["windspeed_10m"]

                results.append({
                    "region": name,
                    "temp": temp,
                    "desc": WEATHER_DESC.get(code, "알 수 없음"),
                    "wind": wind,
                    "travel": judge_travel(temp, code, wind),
                })
            except Exception:
                # 한 지역 실패해도 나머지는 보여주기
                results.append({"region": name, "error": "조회 실패"})

    if all("error" in r for r in results):
        raise HTTPException(503, "날씨 정보를 가져올 수 없습니다")
    return {"items": results}