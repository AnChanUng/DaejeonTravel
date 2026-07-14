<template>
  <header class="header">
    <div class="header-inner">
      <span class="logo" @click="$router.push('/board')">LocalHub</span>
    </div>
  </header>
  <main class="main">
    <router-view />
  </main>
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
