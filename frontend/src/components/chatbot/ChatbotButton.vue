<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import kkumsuniImage from '../../assets/images/mascots/kkumsuni.png'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

import { sendMessage } from "@/api/chatbot";

import kkumsuniImage from "../../assets/images/mascots/kkumsuni.png";

const chatbotOpen = ref(false);
const messages = ref([
  {
    role: "bot",
    content: "안녕하세요! 👋\n궁금한 대전 정보를 물어보세요.",
  },
]);

const input = ref("");

const toggleChatbot = () => {
  chatbotOpen.value = !chatbotOpen.value;
};

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
      content: res.data.answer,
    });
  } catch (e) {
    messages.value.push({
      role: "bot",
      content: "오류가 발생했습니다.",
    });
  }
};

const handleSuggestion = async (question) => {
  input.value = question;
  await handleSend();
};
</script>

<template>
  <div class="chatbot-widget">
    <!-- 채팅창 -->
    <div v-if="chatbotOpen" class="chatbot-widget__panel">
      <header class="chatbot-widget__header">
        <div>
          <strong>{{ t('chatbot.title') }}</strong>

          <span>{{ t('chatbot.description') }}</span>
        </div>

        <button
          type="button"
          :aria-label="t('chatbot.close')"
          @click="toggleChatbot"
        >
          ×
        </button>
      </header>

      <div class="chatbot-widget__body">
        <div class="chatbot-widget__message">
          {{ t('chatbot.greeting') }}
        </div>

        <div class="chatbot-widget__suggestions">
          <button type="button">
            {{ t('chatbot.suggestion1') }}
          </button>

          <button type="button">
            {{ t('chatbot.suggestion2') }}
          </button>

          <button type="button">
            {{ t('chatbot.suggestion3') }}
          </button>
        </div>

        <!-- 실제 대화 -->
        <div
          v-for="(msg, idx) in messages.slice(1)"
          :key="idx"
          :class="[
            'chat-message',
            msg.role === 'user' ? 'chat-message--user' : 'chat-message--bot',
          ]"
        >
          {{ msg.content }}
        </div>
      </div>

      <form class="chatbot-widget__input" @submit.prevent="handleSend">
        <input
          v-model="input"
          type="text"
          :placeholder="t('chatbot.placeholder')"
        >

        <button type="submit">
          {{ t('chatbot.send') }}
        </button>
      </form>
    </div>

    <!-- 챗봇 버튼 -->
    <button
      type="button"
      class="chatbot-widget__button"
      :aria-expanded="chatbotOpen"
      :aria-label="t('chatbot.open')"
      @click="toggleChatbot"
    >
      <img :src="kkumsuniImage" alt="" />

        <span class="chatbot-text">
          {{ t('chatbot.ask') }}
        </span>
    </button>
  </div>
</template>

<style scoped>
.chatbot-widget {
  position: fixed;

  right: 30px;

  bottom: 90px;

  z-index: 100;
}

.chatbot-text {
  white-space: pre-line;
}

/* 버튼 */

.chatbot-widget__button {
  min-width: 160px;

  min-height: 70px;

  padding: 8px 20px 8px 12px;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 10px;

  background: linear-gradient(135deg, #ffe381, #ffc43f);

  border: 1px solid #e5a725;

  border-radius: 999px;

  box-shadow: 0 12px 25px rgba(107, 68, 22, 0.19);

  color: var(--color-brown-900);

  font-weight: 800;

  cursor: pointer;
}

.chatbot-widget__button img {
  width: 52px;

  height: 52px;

  object-fit: contain;
}

.chatbot-widget__button span {
  line-height: 1.3;
}

/* =========================
   채팅창
========================= */

.chatbot-widget__panel {
  position: absolute;

  right: 0;

  bottom: 82px;

  width: 350px;

  height: 470px;

  display: flex;

  flex-direction: column;

  overflow: hidden;

  background: white;

  border: 1px solid var(--color-border);

  border-radius: 20px;

  box-shadow: 0 18px 45px rgba(67, 39, 16, 0.23);
}

.chatbot-widget__header {
  padding: 16px 18px;
  padding: 16px 18px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  background: #f4ad35;
}

.chatbot-widget__header strong,
.chatbot-widget__header span {
  display: block;
}

.chatbot-widget__header span {
  margin-top: 3px;

  font-size: 12px;
}

.chatbot-widget__header button {
  background: transparent;

  border: 0;

  font-size: 27px;

  cursor: pointer;
}

/* =========================
   내용
========================= */

.chatbot-widget__body {
  flex: 1;

  padding: 18px;

  overflow-y: auto;

  background: #fffaf1;
}

.chatbot-widget__message {
  max-width: 85%;

  padding: 12px 14px;

  background: white;

  border-radius: 4px 15px 15px;

  box-shadow: var(--shadow-small);

  font-size: 14px;

  line-height: 1.6;
}

.chatbot-widget__suggestions {
  margin-top: 18px;
  margin-top: 18px;

  display: flex;

  flex-direction: column;

  gap: 8px;
}

.chatbot-widget__suggestions button {
  padding: 10px 12px;
  padding: 10px 12px;

  background: #fff1cf;

  border: 1px solid #e5c085;

  border-radius: 10px;

  text-align: left;

  font-size: 13px;

  cursor: pointer;
}

/* =========================
   입력창
========================= */

.chatbot-widget__input {
  padding: 12px;
  padding: 12px;

  display: flex;

  gap: 8px;

  border-top: 1px solid var(--color-border);
}

.chatbot-widget__input input {
  flex: 1;

  min-width: 0;

  padding: 10px;

  border: 1px solid var(--color-border);

  border-radius: 9px;

  outline: 0;
}

.chatbot-widget__input button {
  padding: 0 15px;
  padding: 0 15px;

  background: var(--color-gold-500);

  border: 0;

  border-radius: 9px;

  font-weight: 700;

  cursor: pointer;
}

/* =========================
   모바일
========================= */

@media (max-width: 600px) {
  .chatbot-widget {
    right: 15px;

    bottom: 75px;
  }

  .chatbot-widget__button {
    min-width: 64px;

    min-height: 64px;

    padding: 5px;
  }

  .chatbot-widget__button img {
    width: 52px;

    height: 52px;
  }

  .chatbot-widget__button span {
    display: none;
    display: none;
  }

  .chatbot-widget__panel {
    position: fixed;

    inset: 0;

    width: auto;

    height: auto;

    border-radius: 0;
  }
}

.chat-message {
  max-width: 80%;
  padding: 12px 16px;
  margin-bottom: 10px;
  border-radius: 18px;
  white-space: pre-line;
  word-break: break-word;
}

.chat-message--bot {
  margin-right: auto;
  background: white;
  color: #333;
  border-radius: 4px 18px 18px 18px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.chat-message--user {
  margin-left: auto;
  background: #f4ad35;
  color: white;
  border-radius: 18px 4px 18px 18px;
}
</style>
