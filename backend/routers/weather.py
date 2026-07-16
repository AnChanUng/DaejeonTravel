import time

from fastapi import APIRouter, HTTPException, Query
import httpx

from translations.weather import (
    WEATHER_DESC,
    REGION_TRANSLATION,
    TRAVEL_TRANSLATION
)


router = APIRouter(
    prefix="/api/weather",
    tags=["weather"]
)


REGIONS = {
    "대전": {"lat": 36.3504, "lng": 127.3845},
    "청주": {"lat": 36.6424, "lng": 127.4890},
    "천안": {"lat": 36.8151, "lng": 127.1139},
    "세종": {"lat": 36.4800, "lng": 127.2890},
}


# ─────────────────────────────────────────────
# 캐시
#
# Open-Meteo 무료 API는 호출 제한이 있고,
# 특히 배포 서버(Render)는 여러 앱이 IP를 공유해
# 간헐적으로 호출이 막히는 문제가 있었다. (503 장애)
#
# 대응:
#   1) 4개 지역을 요청 1번으로 합쳐 호출량을 1/4로 줄이고
#   2) 결과를 10분간 캐싱해 반복 호출을 막고
#   3) 호출이 실패해도 마지막 성공 데이터를 대신 보여준다
#      (사용자는 "10분 전 날씨"라도 보는 게 503보다 낫다)
#
# 캐시에는 언어와 무관한 원시 값(온도/날씨코드/바람)만 저장하고,
# 번역은 응답을 만들 때마다 lang에 맞춰 수행한다.
# ─────────────────────────────────────────────

CACHE_TTL = 600  # 10분

_cache = {
    "data": None,        # {"대전": {"temp":.., "code":.., "wind":..}, ...}
    "fetched_at": 0.0,   # 마지막 성공 시각
}


async def fetch_weather_raw() -> dict:
    """4개 지역 날씨를 Open-Meteo에 한 번의 요청으로 조회한다."""

    lats = ",".join(str(c["lat"]) for c in REGIONS.values())
    lngs = ",".join(str(c["lng"]) for c in REGIONS.values())

    async with httpx.AsyncClient(timeout=8.0) as client:

        res = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lats,
                "longitude": lngs,
                "current": "temperature_2m,weathercode,windspeed_10m",
                "timezone": "Asia/Seoul",
            },
        )
        res.raise_for_status()
        payload = res.json()

    # 좌표를 여러 개 보내면 배열로, 하나면 객체로 오므로 형태를 맞춘다
    if isinstance(payload, dict):
        payload = [payload]

    data = {}

    for name, item in zip(REGIONS.keys(), payload):
        cur = item["current"]
        data[name] = {
            "temp": cur["temperature_2m"],
            "code": cur["weathercode"],
            "wind": cur["windspeed_10m"],
        }

    return data


async def get_weather_data() -> dict:
    """캐시가 유효하면 캐시를, 아니면 새로 조회한다.
    조회 실패 시 오래된 캐시라도 반환하고, 그것도 없으면 예외."""

    now = time.time()

    # 1) 캐시가 아직 신선하면 그대로 사용
    if _cache["data"] and now - _cache["fetched_at"] < CACHE_TTL:
        return _cache["data"]

    # 2) 새로 조회 시도 (일시 오류 대비 1회 재시도)
    for attempt in range(2):
        try:
            data = await fetch_weather_raw()
            _cache["data"] = data
            _cache["fetched_at"] = now
            return data
        except Exception:
            if attempt == 0:
                continue

    # 3) 조회 실패 — 오래된 캐시라도 있으면 그걸 사용 (503 방지)
    if _cache["data"]:
        return _cache["data"]

    # 4) 캐시조차 없으면 그때만 실패 처리
    raise HTTPException(503, "날씨 정보를 가져올 수 없습니다")


def judge_travel(
    temp: float,
    code: int,
    wind: float,
    lang: str
):

    score = 100

    if code >= 95:
        score -= 60
    elif code >= 80:
        score -= 40
    elif code >= 71:
        score -= 30
    elif code >= 61:
        score -= 35
    elif code >= 51:
        score -= 15
    elif code >= 45:
        score -= 10

    if temp >= 33:
        score -= 30
    elif temp >= 30:
        score -= 15
    elif temp <= -10:
        score -= 30
    elif temp <= 0:
        score -= 15

    if wind >= 14:
        score -= 20
    elif wind >= 9:
        score -= 10

    text = TRAVEL_TRANSLATION.get(
        lang,
        TRAVEL_TRANSLATION["ko"]
    )

    if score >= 80:
        return {
            "grade": text["good"],
            "emoji": "😊",
            "comment": text["good_comment"]
        }

    elif score >= 55:
        return {
            "grade": text["normal"],
            "emoji": "🙂",
            "comment": text["normal_comment"]
        }

    else:
        return {
            "grade": text["bad"],
            "emoji": "😷",
            "comment": text["bad_comment"]
        }


@router.get("")
async def get_weather(
    lang: str = Query("ko")
):

    data = await get_weather_data()

    results = []

    for name, w in data.items():
        results.append({
            "region": REGION_TRANSLATION[name][lang],
            "temp": w["temp"],
            "desc": WEATHER_DESC[lang].get(
                w["code"],
                "Unknown"
            ),
            "wind": w["wind"],
            "travel": judge_travel(
                w["temp"],
                w["code"],
                w["wind"],
                lang
            ),
        })

    return {
        "items": results
    }