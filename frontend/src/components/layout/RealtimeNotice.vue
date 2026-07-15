<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import {
  onlineCount,
  connected,
  connectRealtime,
  disconnectRealtime,
} from '../../composables/useRealtime'

// 앱 전체에서 WebSocket 연결을 여기서 한 번만 열고 닫는다.
// (새 게시글 알림은 헤더의 NotificationBell이 같은 연결 상태를 함께 사용)
onMounted(connectRealtime)
onBeforeUnmount(disconnectRealtime)
</script>

<template>
  <div class="online" :class="{ 'online--off': !connected }">
    <span class="online__dot"></span>

    <span v-if="connected">
      지금 <strong>{{ onlineCount }}</strong>명 접속 중
    </span>

    <span v-else>
      연결 중...
    </span>
  </div>
</template>

<style scoped>
/*
  오른쪽 아래 '챗봇에게 물어보기' 버튼과 같은 높이에 오도록 맞춤.
  (챗봇 버튼: bottom 24px / 높이 약 62px → 중앙 정렬 기준 38px)
  챗봇 버튼 위치를 바꾸면 아래 bottom 값도 같이 조정할 것.
*/
.online {
  position: fixed;
  bottom: 38px;
  left: 24px;
  z-index: 90;

  display: flex;
  align-items: center;
  gap: 7px;

  padding: 9px 16px;

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

@media (max-width: 520px) {
  .online {
    bottom: 20px;
    left: 16px;
    padding: 7px 12px;
    font-size: 12px;
  }
}
</style>