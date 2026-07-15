<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import {
  onlineCount,
  connected,
  notices,
  removeNotice,
  connectRealtime,
  disconnectRealtime,
} from '../../composables/useRealtime'

const router = useRouter()

function goPost(notice) {
  removeNotice(notice.id)
  router.push(`/community/${notice.postId}`)
}

onMounted(connectRealtime)
onBeforeUnmount(disconnectRealtime)
</script>

<template>
  <div class="realtime">

    <!-- 새 게시글 알림 -->
    <TransitionGroup name="toast" tag="div" class="realtime__toasts">
      <button
        v-for="notice in notices"
        :key="notice.id"
        class="toast"
        @click="goPost(notice)"
      >
        <span class="toast__icon">🔔</span>

        <span class="toast__body">
          <span class="toast__label">
            새 글 · {{ notice.category }}
          </span>

          <span class="toast__title">
            {{ notice.title }}
          </span>
        </span>

        <span
          class="toast__close"
          @click.stop="removeNotice(notice.id)"
        >
          ×
        </span>
      </button>
    </TransitionGroup>

    <!-- 접속자 현황 -->
    <div class="online" :class="{ 'online--off': !connected }">
      <span class="online__dot"></span>

      <span v-if="connected">
        지금 <strong>{{ onlineCount }}</strong>명 접속 중
      </span>

      <span v-else>
        연결 중...
      </span>
    </div>

  </div>
</template>

<style scoped>
/* 챗봇 버튼이 오른쪽 아래에 있어 왼쪽 아래에 배치 */
.realtime {
  position: fixed;
  bottom: 24px;
  left: 24px;
  z-index: 90;

  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
}

.realtime__toasts {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 새 글 토스트 */
.toast {
  display: flex;
  align-items: center;
  gap: 10px;

  width: 290px;
  padding: 12px 14px;

  background: var(--color-cream-100);
  border: 1px solid #e5c085;
  border-radius: 16px;
  box-shadow: var(--shadow-medium);

  cursor: pointer;
  text-align: left;
  transition: transform 0.15s ease;
}

.toast:hover {
  transform: translateY(-2px);
}

.toast__icon {
  flex-shrink: 0;
  font-size: 18px;
}

.toast__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toast__label {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-brown-500);
}

.toast__title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-brown-900);

  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.toast__close {
  flex-shrink: 0;
  padding: 0 2px;
  color: var(--color-brown-500);
  font-size: 17px;
}

/* 접속자 배지 */
.online {
  display: flex;
  align-items: center;
  gap: 7px;

  padding: 7px 14px;

  background: rgba(255, 253, 248, 0.94);
  border: 1px solid #ddc49e;
  border-radius: 999px;
  box-shadow: var(--shadow-small);
  backdrop-filter: blur(6px);

  font-size: 13px;
  color: var(--color-brown-700);
}

.online strong {
  color: var(--color-brown-900);
  font-weight: 800;
}

.online__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #1b8f5a;
  animation: pulse 2s ease-in-out infinite;
}

.online--off .online__dot {
  background: #b99b74;
  animation: none;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.35;
  }
}

/* 토스트 등장 / 퇴장 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

@media (max-width: 520px) {
  .realtime {
    bottom: 16px;
    left: 16px;
  }

  .toast {
    width: 240px;
  }
}
</style>