import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "", // 로컬은 빈값→프록시, 배포는 Render주소
});

export default api;
