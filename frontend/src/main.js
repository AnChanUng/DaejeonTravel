import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";

import "./assets/styles/reset.css";
import "./assets/styles/global.css";

import "./style.css";

// ✅ Kakao SDK 초기화
window.Kakao.init(import.meta.env.VITE_KAKAO_JS_KEY);

// (선택) 정상 초기화 확인
console.log("Kakao initialized:", window.Kakao.isInitialized());

createApp(App).use(router).mount("#app");
