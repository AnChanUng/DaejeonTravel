<script setup>
import { ref } from "vue";
import { sendMessage } from "@/api/chatbot";

const isOpen = ref(false);

const input = ref("");
const messages = ref([
  {
    role: "bot",
    content: "안녕하세요! LocalHub 챗봇입니다 😊",
  },
]);

const handleSend = async () => {
  if (!input.value.trim()) return;

  const text = input.value;

  messages.value.push({
    role: "user",
    content: text,
  });

  input.value = "";

  try {
    const res = await sendMessage(text);

    messages.value.push({
      role: "bot",
      content: res.answer, // 백엔드 응답에 맞게 수정
    });
  } catch (e) {
    messages.value.push({
      role: "bot",
      content: "죄송합니다. 오류가 발생했습니다.",
    });
  }
};
</script>

<template>
  <!-- 채팅창 -->
  <div v-if="isOpen" class="chat-window">
    <div class="chat-header">
      <span>🤖 LocalHub 챗봇</span>

      <button @click="isOpen = false">✕</button>
    </div>

    <div class="chat-body">
      <div v-for="(msg, idx) in messages" :key="idx" :class="msg.role">
        {{ msg.content }}
      </div>
    </div>

    <div class="chat-footer">
      <input v-model="input" @keyup.enter="handleSend" placeholder="메시지를 입력하세요." />

      <button @click="handleSend">전송</button>
    </div>
  </div>

  <!-- 플로팅 버튼 -->
  <button v-if="!isOpen" class="floating-btn" @click="isOpen = true">💬</button>
</template>

<style scoped>
.floating-btn {
  position: fixed;
  right: 25px;
  bottom: 25px;

  width: 60px;
  height: 60px;

  border: none;
  border-radius: 50%;

  background: #4f46e5;
  color: white;

  font-size: 26px;
  cursor: pointer;

  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.chat-window {
  position: fixed;
  right: 25px;
  bottom: 25px;

  width: 360px;
  height: 520px;

  background: white;
  border-radius: 16px;

  display: flex;
  flex-direction: column;

  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.chat-header {
  background: #4f46e5;
  color: white;

  padding: 14px 16px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header button {
  border: none;
  background: transparent;
  color: white;
  cursor: pointer;
  font-size: 18px;
}

.chat-body {
  flex: 1;

  padding: 15px;

  overflow-y: auto;

  background: #f5f5f5;
}

.user {
  text-align: right;

  background: #4f46e5;
  color: white;

  padding: 10px;
  border-radius: 10px;

  margin-bottom: 10px;
}

.bot {
  text-align: left;

  background: white;

  padding: 10px;
  border-radius: 10px;

  margin-bottom: 10px;
}

.chat-footer {
  display: flex;

  padding: 10px;

  border-top: 1px solid #ddd;
}

.chat-footer input {
  flex: 1;

  padding: 10px;

  border: 1px solid #ddd;
  border-radius: 8px;
}

.chat-footer button {
  margin-left: 8px;

  padding: 10px 16px;

  border: none;

  background: #4f46e5;
  color: white;

  border-radius: 8px;

  cursor: pointer;
}
</style>
