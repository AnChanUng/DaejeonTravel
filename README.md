# 🥐 대전이야기

> 공공데이터 기반 대전·충청 지역 정보 공유 커뮤니티

관광지, 음식점, 숙박, 축제 정보를 한눈에 보고, 지역 이야기를 나누는 여행 커뮤니티 서비스입니다.
한국관광공사 TourAPI 4.0 공공데이터(대전·세종·충남·충북)를 활용했습니다.

---

## 📌 주요 기능

| 기능 | 설명 |
|---|---|
| 메인 페이지 | 권역 소개 히어로, 장소 통합 검색(자동완성), 추천 관광지 캐러셀, 오늘의 날씨 |
| 장소 정보 | 관광지 · 음식점 · 숙박 목록/상세, 권역 필터, 검색, 카카오맵 위치 링크 |
| 커뮤니티 | 게시글 CRUD, 비밀번호 기반 수정·삭제, 카테고리 필터 |
| 지역 정보 챗봇 | Gemini API 기반 관광지 추천 · 축제 일정 · 음식점 질의응답 |
|---|---|
| 🎪 축제 캘린더 — 월간 캘린더, 지역별 색상, 상세 모달 | FullCalendar |
| ☀️ 날씨 연동 — 4개 권역 실시간 날씨 + 여행 적합도 | Open-Meteo API |
| 🌐 다국어 지원 — 한국어/English 전환 | vue-i18n |
| 🗺️ 지도 시각화 — 851곳 핀 표시, 유형·권역 필터 | Leaflet.js + OpenStreetMap |
| 🚗 경로 안내 — 최대 8곳 선택, 도로 경로 · 거리 · 소요시간 | OSRM |
| 📊 대시보드 — 게시글/장소 통계 차트 4종 | Chart.js |
| 🔔 실시간 알림 — 새 글 알림함, 접속자 수, 탭 제목 배지 | FastAPI WebSocket |
| 📝 게시판 확장 — 조회수, 태그, 좋아요, 북마크, 이미지 첨부, 통합 검색 | FastAPI StaticFiles |

---

## 🛠 기술 스택

| 구분 | 기술 |
|---|---|
| Frontend | Vue.js 3 (Vite), Vue Router, vue-i18n, Axios |
| Backend | FastAPI, SQLAlchemy, SQLite, WebSocket |
| 시각화 | Leaflet.js, FullCalendar, Chart.js |
| AI | Gemini API |
| 배포 | Vercel (FE) · Render (BE) |

## 🏗 아키텍처 특징

- **정적 데이터는 JSON 직독 + 메모리 캐싱**: 장소 데이터(1,300여 건)는 사용자가 수정하지 않는 읽기 전용 데이터이므로 DB 대신 JSON을 직접 읽고 `lru_cache`로 캐싱 — 팀원 누구나 clone 후 바로 실행 가능
- **동적 데이터만 DB 저장**: 사용자가 생성하는 게시글만 SQLite에 저장, DB 파일은 gitignore 처리
- **실시간 통신**: WebSocket ConnectionManager로 접속자 관리 + 새 글 브로드캐스트, 자동 재연결 처리

---

## 🚀 실행 방법

### 1. 백엔드
```bash
cd backend
source .venv/Scripts/activate        
uvicorn main:app --reload --port 8000
```

### 2. 프론트엔드
```bash
cd frontend
npm run dev                          # http://localhost:5173
```

---

## 📁 프로젝트 구조

```
├── backend/
│   ├── main.py                # FastAPI 앱, 라우터 등록
│   ├── models.py              # Post 모델 (게시글)
│   ├── data/대전_충청권/       # 공공데이터 JSON (관광지·음식점·숙박·축제)
│   └── routers/
│       ├── locations.py       # 장소 조회 (JSON 캐싱, 자동완성, 지도용 좌표)
│       ├── posts.py           # 게시판 CRUD + 좋아요·북마크·이미지 업로드
│       ├── festivals.py       # 축제 캘린더
│       ├── weather.py         # 날씨 + 여행 적합도
│       ├── stats.py           # 대시보드 통계
│       ├── chatbot.py         # Gemini 챗봇
│       └── ws.py              # WebSocket 실시간 알림
└── frontend/
    └── src/
        ├── views/             # 페이지 (장소·게시판·캘린더·지도·대시보드)
        ├── components/        # 공통 컴포넌트 (헤더·알림함·챗봇 등)
        ├── composables/       # useRealtime (WebSocket 연결 관리)
        └── locales/           # 다국어 리소스
```

---
