<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import {
  notifications,
  unreadCount,
  markAllRead,
  clearNotifications,
  timeAgo,
} from '../../composables/useRealtime'

const router = useRouter()

const open = ref(false)
const shaking = ref(false)
const rootEl = ref(null)

// 새 알림이 오면 종을 한 번 흔들어준다.
watch(unreadCount, (next, prev) => {
  if (next > prev) {
    shaking.value = true
    setTimeout(() => (shaking.value = false), 900)
  }
})

function toggle() {
  open.value = !open.value

  // 알림함을 열면 읽음 처리
  if (open.value) {
    markAllRead()
  }
}

function goPost(notice) {
  open.value = false
  router.push(`/community/${notice.postId}`)
}

function onClickOutside(event) {
  if (open.value && rootEl.value && !rootEl.value.contains(event.target)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div ref="rootEl" class="bell">

    <button
      type="button"
      class="bell__button"
      :class="{ 'bell__button--shake': shaking }"
      :aria-expanded="open"
      aria-label="알림"
      @click="toggle"
    >
      <span aria-hidden="true">🔔</span>

      <span
        v-if="unreadCount > 0"
        class="bell__badge"
      >
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </span>
    </button>

    <div v-if="open" class="bell__panel">

      <div class="bell__head">
        <strong>알림</strong>

        <button
          v-if="notifications.length"
          type="button"
          class="bell__clear"
          @click="clearNotifications"
        >
          전체 삭제
        </button>
      </div>

      <div v-if="notifications.length" class="bell__list">
        <button
          v-for="notice in notifications"
          :key="notice.id"
          type="button"
          class="bell__item"
          @click="goPost(notice)"
        >
          <span class="bell__item-category">
            {{ notice.category }}
          </span>

          <span class="bell__item-title">
            {{ notice.title }}
          </span>

          <span class="bell__item-time">
            {{ timeAgo(notice.at) }}
          </span>
        </button>
      </div>

      <p v-else class="bell__empty">
        아직 새 소식이 없어요
      </p>

    </div>

  </div>
</template>

<style scoped>
.bell {
  position: relative;
}

.bell__button {
  position: relative;
  width: 40px;
  height: 40px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #fffaf0;
  border: 1px solid #ddc49e;
  border-radius: 50%;

  font-size: 17px;
  cursor: pointer;
}

.bell__button:hover {
  background: #fff2d7;
}

/* 새 알림이 오면 종이 흔들림 */
.bell__button--shake {
  animation: shake 0.9s ease;
}

@keyframes shake {
  0%,
  100% {
    transform: rotate(0);
  }
  15% {
    transform: rotate(14deg);
  }
  30% {
    transform: rotate(-12deg);
  }
  45% {
    transform: rotate(9deg);
  }
  60% {
    transform: rotate(-7deg);
  }
  75% {
    transform: rotate(4deg);
  }
}

.bell__badge {
  position: absolute;
  top: -3px;
  right: -3px;

  min-width: 17px;
  height: 17px;
  padding: 0 4px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #d94f3d;
  border: 1.5px solid #fffdf8;
  border-radius: 999px;

  color: #fff;
  font-size: 10px;
  font-weight: 800;
  line-height: 1;
}

/* 드롭다운 */
.bell__panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  z-index: 60;

  width: 300px;
  padding: 8px;

  background: #fffdf8;
  border: 1px solid var(--color-border);
  border-radius: 14px;
  box-shadow: var(--shadow-medium);
}

.bell__head {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 6px 8px 10px;
  border-bottom: 1px solid #f0deba;
}

.bell__head strong {
  color: var(--color-brown-900);
  font-size: 14px;
  font-weight: 800;
}

.bell__clear {
  background: transparent;
  border: 0;
  color: var(--color-brown-500);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.bell__clear:hover {
  color: #c0392b;
}

.bell__list {
  max-height: 300px;
  overflow-y: auto;
  padding-top: 6px;
}

.bell__item {
  width: 100%;
  padding: 10px;

  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-rows: auto auto;
  gap: 2px 8px;

  background: transparent;
  border: 0;
  border-radius: 10px;

  text-align: left;
  cursor: pointer;
}

.bell__item:hover {
  background: #fff1cf;
}

.bell__item-category {
  grid-column: 1;
  padding: 2px 8px;

  background: var(--color-cream-300);
  border: 1px solid #e5c085;
  border-radius: 999px;

  color: var(--color-brown-700);
  font-size: 10px;
  font-weight: 700;
  white-space: nowrap;
}

.bell__item-time {
  grid-column: 2;
  color: var(--color-brown-500);
  font-size: 11px;
}

.bell__item-title {
  grid-column: 1 / -1;
  grid-row: 2;

  overflow: hidden;
  color: var(--color-brown-900);
  font-size: 13px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bell__empty {
  padding: 26px 0;
  color: var(--color-brown-500);
  font-size: 13px;
  text-align: center;
}
</style>