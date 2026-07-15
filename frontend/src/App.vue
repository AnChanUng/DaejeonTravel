<script setup>
import RealtimeNotice from './components/layout/RealtimeNotice.vue'
</script>

<template>
  <RouterView />

  <!-- 실시간 알림 (접속자 수 + 새 게시글 토스트) -->
  <RealtimeNotice />
</template>

<style scoped>
.header {
  background: var(--color-card);
  border-bottom: 1px solid var(--color-bg);
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-inner {
  max-width: 720px;
  margin: 0 auto;
  padding: 16px 20px;
}
.logo {
  font-size: 20px;
  font-weight: 800;
  color: var(--color-primary);
  cursor: pointer;
  letter-spacing: -0.5px;
}
.main {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px 20px 60px;
}
</style>