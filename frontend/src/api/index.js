import axios from "axios";

// 배포 환경에선 .env.production의 주소를, 로컬 개발에선 로컬 백엔드를 사용
const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
