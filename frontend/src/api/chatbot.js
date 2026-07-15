import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const sendMessage = (message) => {
  return api.post("/api/chat", {
    message,
  });
};
