<script setup>
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
import ChatbotButton from '../chatbot/ChatbotButton.vue'
</script>

<template>
  <div class="page-layout">

    <AppHeader />

    <main class="page-layout__main">
      <div class="page-layout__inner">
        <slot />
      </div>
    </main>

    <AppFooter />

    <ChatbotButton />

  </div>
</template>

<style scoped>
.page-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background:
    linear-gradient(
      180deg,
      #fff3da 0%,
      var(--color-cream-200) 260px,
      var(--color-cream-100) 100%
    );
}

.page-layout__main {
  flex: 1;
  width: 100%;
}

.page-layout__inner {
  width: min(880px, 100%);
  margin: 0 auto;
  padding: 44px 20px 90px;
}

@media (max-width: 520px) {
  .page-layout__inner {
    padding: 28px 16px 60px;
  }
}
</style>