import json
import re

from google import genai
from pathlib import Path
from config import settings
from chatbot.prompt import SYSTEM_PROMPT

# 검색에 방해되는 조사/의존명사/불용어
STOPWORDS = {
    "은", "는", "이", "가", "을", "를", "에", "에서", "의", "와", "과",
    "도", "만", "로", "으로", "이랑", "랑", "한테", "께", "부터", "까지",
    "좀", "알려줘", "추천해줘", "추천", "찾아줘", "뭐야", "뭐가", "있어",
    "있나요", "있나", "어디", "어디야", "어디에", "어떤", "곳", "좋을까",
    "싶어", "싶은데", "해줘", "줘", "요", "?", ".", ",", "!"
}

def extract_keywords(question: str) -> list[str]:
    """
    질문 문장에서 검색에 사용할 키워드를 추출한다.
    - 특수문자 제거
    - 공백 기준 분리
    - 불용어 제거
    - 2글자 미만 토큰(조사 등)은 버림
    """
    # 특수문자 제거 (한글, 영문, 숫자, 공백만 남김)
    cleaned = re.sub(r"[^가-힣a-zA-Z0-9\s]", " ", question)

    words = cleaned.split()

    keywords = [
        w for w in words
        if w not in STOPWORDS and len(w) >= 2
    ]

    # 키워드가 하나도 안 걸리면 원본 단어라도 반환 (검색 결과 0건 방지)
    return keywords if keywords else words

# ai
client = genai.Client(
    api_key=settings.gemini_api_key
)

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
    검색된 데이터를 Gemini에게 전달할 문자열로 변환
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

def build_prompt(question: str, context: str) -> str:
    return f"""
            {SYSTEM_PROMPT}

            ==========================
            사용자 질문
            ==========================

            {question}

            ==========================
            참고 데이터
            ==========================

            {context}

            ==========================
            답변 작성 규칙
            ==========================

            - 반드시 참고 데이터 안에서만 답변한다.
            - 없는 정보는 추측하지 않는다.
            - 필요한 경우 목록 형태로 정리한다.
            - 자연스럽고 친절한 한국어로 답변한다.
            """

def ask_chatbot(question: str):
    """
    사용자 질문을 받아
    1. 데이터셋 선택
    2. JSON 검색
    3. Context 생성
    4. Gemini에게 전달
    """

    dataset = select_dataset(question)

    results = search_data(dataset, question)

    if not results:
        return "제공된 데이터에서 관련 정보를 찾을 수 없습니다."

    context = build_context(results)

    prompt = build_prompt(question, context)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if hasattr(response, "text") and response.text:
            return response.text

        return str(response)

    except Exception as e:
        print("Gemini Error:", e)
        return "AI 응답 생성 중 오류가 발생했습니다."
    