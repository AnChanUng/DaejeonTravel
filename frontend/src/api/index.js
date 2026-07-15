import axios from "axios";

// Vercel 배포 환경 변수가 없을 경우를 대비해 Render 배포 주소를 기본값(Fallback)으로 지정합니다.
const API_URL =
  import.meta.env.VITE_API_BASE_URL || "https://localhub-7ql5.onrender.com";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
