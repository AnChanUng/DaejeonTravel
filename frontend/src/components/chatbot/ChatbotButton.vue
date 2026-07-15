<script setup>
import { ref, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { sendMessage } from '@/api/chatbot'

import kkumsuniImage from '../../assets/images/mascots/kkumsuni.png'

const { t, locale } = useI18n()

const chatbotOpen = ref(false)
const messages = ref([])
const input = ref('')
const sending = ref(false)
const chatBody = ref(null)

const scrollToBottom = async () => {
  await nextTick()

  if (chatBody.value) {
    chatBody.value.scrollTop = chatBody.value.scrollHeight
  }
}

const toggleChatbot = async () => {
  chatbotOpen.value = !chatbotOpen.value

  if (chatbotOpen.value) {
    await scrollToBottom()
  }
}

const handleSend = async () => {
  const text = input.value.trim()

  if (!text || sending.value) {
    return
  }

  messages.value.push({
    role: 'user',
    content: text
  })

  input.value = ''
  sending.value = true

  await scrollToBottom()

  try {
    const response = await sendMessage(text, locale.value)

    const answer =
      response?.data?.answer ??
      response?.answer ??
      t('chatbot.error', '오류가 발생했습니다. 잠시 후 다시 시도해주세요.')

    messages.value.push({
      role: 'bot',
      content: answer
    })
  } catch (error) {
    console.error('챗봇 요청 실패:', error)

    messages.value.push({
      role: 'bot',
      content: t(
        'chatbot.error',
        '오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
      )
    })
  } finally {
    sending.value = false
    await scrollToBottom()
  }
}

const handleSuggestion = async (question) => {
  input.value = question
  await handleSend()
}
</script>

<template>
  <div class="chatbot-widget">
    <div
      v-if="chatbotOpen"
      class="chatbot-widget__panel"
    >
      <header class="chatbot-widget__header">
        <div>
          <strong>
            {{ t('chatbot.title') }}
          </strong>

          <span>
            {{ t('chatbot.description') }}
          </span>
        </div>

        <button
          type="button"
          :aria-label="t('chatbot.close')"
          @click="toggleChatbot"
        >
          ×
        </button>
      </header>

      <div
        ref="chatBody"
        class="chatbot-widget__body"
      >
        <div class="chatbot-widget__message">
          {{ t('chatbot.greeting') }}
        </div>

        <div
          v-if="messages.length === 0"
          class="chatbot-widget__suggestions"
        >
          <button
            type="button"
            @click="handleSuggestion(t('chatbot.suggestion1'))"
          >
            {{ t('chatbot.suggestion1') }}
          </button>

          <button
            type="button"
            @click="handleSuggestion(t('chatbot.suggestion2'))"
          >
            {{ t('chatbot.suggestion2') }}
          </button>

          <button
            type="button"
            @click="handleSuggestion(t('chatbot.suggestion3'))"
          >
            {{ t('chatbot.suggestion3') }}
          </button>
        </div>

        <div
          v-if="messages.length > 0"
          class="chatbot-widget__conversation"
        >
          <div
            v-for="(msg, idx) in messages"
            :key="`${msg.role}-${idx}`"
            :class="[
              'chat-message',
              msg.role === 'user'
                ? 'chat-message--user'
                : 'chat-message--bot'
            ]"
          >
            {{ msg.content }}
          </div>
        </div>

        <div
          v-if="sending"
          class="chat-message chat-message--bot chatbot-widget__typing"
        >
          ...
        </div>
      </div>

      <form
        class="chatbot-widget__input"
        @submit.prevent="handleSend"
      >
        <input
          v-model="input"
          type="text"
          :placeholder="t('chatbot.placeholder')"
          :disabled="sending"
        >

        <button
          type="submit"
          :disabled="sending || !input.trim()"
        >
          {{ sending ? '...' : t('chatbot.send') }}
        </button>
      </form>
    </div>

    <button
      type="button"
      class="chatbot-widget__button"
      :aria-expanded="chatbotOpen"
      :aria-label="t('chatbot.open')"
      @click="toggleChatbot"
    >
      <img
        :src="kkumsuniImage"
        alt=""
      >

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

/* 챗봇 열기 버튼 */

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

/* 채팅창 */

.chatbot-widget__panel {
  position: absolute;
  right: 0;
  bottom: 82px;

  width: 350px;
  height: 470px;

  display: flex;
  flex-direction: column;
  overflow: hidden;

  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: 20px;

  box-shadow: 0 18px 45px rgba(67, 39, 16, 0.23);
}

.chatbot-widget__header {
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

.chatbot-widget__header strong {
  color: var(--color-brown-900);
}

.chatbot-widget__header span {
  margin-top: 3px;
  color: var(--color-brown-800);
  font-size: 12px;
}

.chatbot-widget__header button {
  padding: 0;

  background: transparent;
  border: 0;

  color: var(--color-brown-900);
  font-size: 27px;
  line-height: 1;
  cursor: pointer;
}

/* 채팅 내용 */

.chatbot-widget__body {
  flex: 1;
  padding: 18px;
  overflow-y: auto;
  background: #fffaf1;
}

.chatbot-widget__message {
  max-width: 85%;
  padding: 12px 14px;

  background: #ffffff;
  border-radius: 4px 15px 15px;
  box-shadow: var(--shadow-small);

  font-size: 14px;
  line-height: 1.6;
  white-space: pre-line;
}

.chatbot-widget__suggestions {
  margin-top: 18px;

  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chatbot-widget__suggestions button {
  padding: 10px 12px;

  background: #fff1cf;
  border: 1px solid #e5c085;
  border-radius: 10px;

  color: var(--color-brown-900);
  text-align: left;
  font-size: 13px;

  cursor: pointer;
}

.chatbot-widget__suggestions button:hover {
  background: #ffe8b5;
}

/* 인사말과 실제 대화 사이 간격 */

.chatbot-widget__conversation {
  margin-top: 10px;
}

.chat-message {
  max-width: 80%;
  margin-bottom: 10px;
  padding: 12px 16px;

  border-radius: 18px;

  white-space: pre-line;
  word-break: break-word;
  font-size: 14px;
  line-height: 1.5;
}

.chat-message--bot {
  margin-right: auto;

  background: #ffffff;
  color: #333333;
  border-radius: 4px 18px 18px 18px;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.chat-message--user {
  margin-left: auto;

  background: #f4ad35;
  color: #ffffff;
  border-radius: 18px 4px 18px 18px;
}

.chatbot-widget__typing {
  margin-top: 10px;
}

/* 입력창 */

.chatbot-widget__input {
  padding: 12px;

  display: flex;
  gap: 8px;

  background: #ffffff;
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

.chatbot-widget__input input:focus {
  border-color: var(--color-gold-500);
}

.chatbot-widget__input button {
  padding: 0 15px;

  background: var(--color-gold-500);
  border: 0;
  border-radius: 9px;

  color: var(--color-brown-900);
  font-weight: 700;
  cursor: pointer;
}

.chatbot-widget__input button:disabled,
.chatbot-widget__input input:disabled {
  cursor: default;
  opacity: 0.65;
}

/* 모바일 */

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
  }

  .chatbot-widget__panel {
    position: fixed;
    inset: 0;

    width: auto;
    height: auto;

    border-radius: 0;
  }
}
</style>