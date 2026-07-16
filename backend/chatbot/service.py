import json
import re
import copy

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
    "싶어", "싶은데", "해줘", "줘", "요", "추천", "알려줘", "찾아줘", "좋은",
    "있어", "가고싶어", "갈만한", "어디", "?", ".", ",", "!"
}

LOCATION_ALIAS = {
    # 주요 역
    "대전역": "중동",
    "서대전역": "오류동",
    "신탄진역": "신탄진동",

    # 터미널
    "대전복합터미널": "용전동",
    "유성터미널": "구암동",

    # 유명 장소
    "성심당": "은행동",
    "한밭수목원": "만년동",
    "오월드": "산성동",
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

def replace_location_alias(question: str) -> str:
    """
    사용자가 입력한 유명 장소명을
    검색 가능한 행정구역으로 변환
    """

    for alias, region in LOCATION_ALIAS.items():
        question = question.replace(alias, region)

    return question

def select_datasets(question: str):
    datasets = []

    # 숙소
    if any(keyword in question for keyword in [
        "숙소", "호텔", "모텔", "펜션", "게스트하우스", "숙박"
    ]):
        datasets.append("숙박")


    # 음식점
    if any(keyword in question for keyword in [
        "음식점", "먹거리", "음식", "맛집", "식당", "카페", "먹을", "밥"
    ]):
        datasets.append("음식점")


    # 관광지
    if any(keyword in question for keyword in [
        "관광", "관광지", "명소", "볼거리", "여행지", "가볼만한곳",
        "놀거리", "데이트", "산책", "공원", "전시", "박물관", "체험"
    ]):
        datasets.append("관광지")

    # 키워드가 없으면 전체 검색
    if not datasets:
        datasets = ["숙박", "음식점", "관광지"]

    return datasets


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
            new_item = copy.deepcopy(item)
            new_item["category"] = dataset
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    
    if scored:
        return [item for _, item in scored[:limit]]
    
    # 검색 결과가 없을 경우 기본 추천
    default_items = []
    for item in items[:limit]:
        new_item = copy.deepcopy(item)
        new_item["category"] = dataset
        default_items.append(new_item)

    return default_items
    # return items[:limit]

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
            카테고리: {item.get("category", "")}
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
            - 사용자가 요청한 카테고리만 답변한다.
            - 요청하지 않은 카테고리는 언급하지 않는다.
            - 요청한 카테고리 중 참고 데이터가 없는 경우에만 데이터가 없다고 표시한다.
            - 숙소, 음식점, 관광지 등 여러 카테고리를 요청하면 각각 구분해서 작성한다.

            답변 형식 예시:

            ## 숙소 추천
            - 이름:
            - 주소:
            - 소개:

            ## 음식점 추천
            - 이름:
            - 주소:
            - 소개:

            ## 관광지 추천
            - 이름:
            - 주소:
            - 소개:
            """

def ask_chatbot(question: str):
    """
    사용자 질문을 받아
    1. 데이터셋 선택
    2. JSON 검색
    3. Context 생성
    4. Gemini에게 전달
    """
    original_question = question

    search_question = replace_location_alias(question)

    datasets = select_datasets(search_question)

    results = []

    for dataset in datasets:
        data = search_data(dataset, search_question)

        for item in data:
            item["category"] = dataset

        results.extend(data)

    if not results:
        return "제공된 데이터에서 관련 정보를 찾을 수 없습니다."

    context = build_context(results)

    prompt = build_prompt(original_question, context)

    try:
        response = client.models.generate_content(
            model="models/gemini-3.1-flash-lite",
            contents=prompt,
        )
        '''hasattr(response, "text") and '''

        if response.text: 
            return response.text

        return str(response)

    except Exception as e:
        print("Gemini Error:", e)
        return "AI 응답 생성 중 오류가 발생했습니다."
    
