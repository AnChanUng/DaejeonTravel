<template>
  <footer class="app-footer">
    <div class="app-footer__inner">
      <div class="app-footer__brand">
        <strong>대전이야기</strong>
        <span>DAEJEON LOCAL COMMUNITY</span>
      </div>

      <span class="app-footer__divider" />

      <p>
        본 서비스는 대전광역시 공공데이터를 활용하여 제작되었습니다.
      </p>

      <span class="app-footer__divider" />

      <p>
        © 2026 Daejeon Story. All rights reserved.
      </p>

      <span
        class="app-footer__bread"
        aria-hidden="true"
      >
        🥐
      </span>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  padding: 18px 20px;

  background: rgba(255, 250, 239, 0.92);
  border-top: 1px solid #ead6b6;
}

.app-footer__inner {
  width: min(980px, 100%);
  margin: 0 auto;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;

  color: #8b6e56;
  font-size: 12px;
}

.app-footer__brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-footer__brand strong {
  color: var(--color-brown-800);
  font-size: 15px;
}

.app-footer__brand span {
  font-size: 10px;
}

.app-footer__divider {
  width: 1px;
  height: 15px;

  background: #d8bd97;
}

.app-footer__bread {
  font-size: 20px;
}

@media (max-width: 800px) {
  .app-footer__inner {
    flex-direction: column;
    gap: 8px;

    text-align: center;
  }

  .app-footer__divider {
    display: none;
  }
}
</style>