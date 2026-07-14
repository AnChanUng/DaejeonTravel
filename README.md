## 실행 방법

### Backend
```
cd backend
python -m venv .venv
source .venv/Scripts/activate      
pip install -r requirements.txt
cp .env.example .env               # .env 열어서 값 채우기
uvicorn main:app --reload --port 8000
```

### Frontend
cd frontend
npm install
npm run dev

## 접속
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:5173
