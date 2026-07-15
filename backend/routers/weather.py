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


def judge_travel(
    temp: float,
    code: int,
    wind: float,
    lang: str
):

    score = 100
    reasons = []


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

                    "region": REGION_TRANSLATION[name][lang],

                    "temp": temp,

                    "desc": WEATHER_DESC[lang].get(
                        code,
                        "Unknown"
                    ),

                    "wind": wind,

                    "travel": judge_travel(
                        temp,
                        code,
                        wind,
                        lang
                    )

                })


            except Exception:

                results.append({
                    "region": REGION_TRANSLATION[name][lang],
                    "error": "조회 실패"
                })


    if all("error" in r for r in results):
        raise HTTPException(
            503,
            "날씨 정보를 가져올 수 없습니다"
        )


    return {
        "items": results
    }