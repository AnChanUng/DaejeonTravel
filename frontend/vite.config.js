import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },

  server: {
    proxy: {
      "/api": "http://localhost:8000",

      // WebSocket은 ws: true 를 켜줘야 프록시가 연결을 넘겨준다.
      "/ws": {
        target: "ws://localhost:8000",
        ws: true,
      },
    },
  },
});
