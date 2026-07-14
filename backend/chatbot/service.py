import json
from pathlib import Path

from openai import OpenAI

from config import settings
from chatbot.prompt import SYSTEM_PROMPT


client = OpenAI(api_key=settings.openai_api_key)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "대전_충청권"

DATA_FILES = {
    "관광지": "대전_충청권_관광지.json",
    "음식점": "대전_충청권_음식점.json",
    "숙박": "대전_충청권_숙박.json",
}


def load_json(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


# 서버 시작 시 한 번만 메모리에 저장
DATA = {
    key: load_json(file)
    for key, file in DATA_FILES.items()
}

def select_dataset(question: str):
    question = question.strip()

    if any(keyword in question for keyword in [
        "음식", "맛집", "식당", "카페", "먹을", "밥"
    ]):
        return "음식점"

    if any(keyword in question for keyword in [
        "숙박", "호텔", "펜션", "모텔", "게스트하우스"
    ]):
        return "숙박"

    return "관광지"

def search_data(dataset: str, question: str, limit=5):
    items = DATA[dataset]["items"]

    keywords = extract_keywords(question)

    scored = []

    for item in items:

        score = 0

        title = str(item.get("title", ""))
        addr = str(item.get("addr1", ""))
        overview = str(item.get("overview", ""))

        for keyword in keywords:

            if keyword in title:
                score += 5

            if keyword in addr:
                score += 4

            if keyword in overview:
                score += 1

        if score > 0:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [item for _, item in scored[:limit]]

def build_context(results):
    """
    검색된 데이터를 GPT에게 전달할 문자열로 변환
    """

    if not results:
        return "관련 데이터가 없습니다."

    contexts = []

    for item in results:
        contexts.append(
            f"""
이름: {item.get("title", "")}
주소: {item.get("addr1", "")}
소개: {item.get("overview", "")}
전화번호: {item.get("tel", "")}
""".strip()
        )

    return "\n\n".join(contexts)

def ask_chatbot(question: str):
    dataset = select_dataset(question)

    results = search_data(dataset, question)

    if not results:
        return "제공된 데이터에서 찾을 수 없습니다."

    context = build_context(results)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
질문:
{question}

참고 데이터:
{context}
""",
            },
        ],
    )

    return response.output_text