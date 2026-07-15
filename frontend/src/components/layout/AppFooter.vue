<template>
  <footer class="app-footer">
    <div class="app-footer__inner">
      <div class="app-footer__brand">
        <strong>대전이야기</strong>
        <span>DAEJEON LOCAL COMMUNITY</span>
      </div>

      <span class="app-footer__divider"></span>

      <p>본 서비스는 대전광역시 공공데이터를 활용하여 제작되었습니다.</p>

      <span class="app-footer__divider"></span>

      <p>© 2026 Daejeon Story. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  position: static;
  width: 100%;
  margin-top: 32px;
  padding: 20px 24px;
  box-sizing: border-box;
  background: #fffaf0;
  border-top: 1px solid #e8c98c;
}

.app-footer__inner {
  width: min(1100px, 100%);
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
  color: #806040;
  font-size: 12px;
}

.app-footer__brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-footer__brand strong {
  font-size: 15px;
  color: #5b3518;
}

.app-footer__brand span {
  font-size: 10px;
}

.app-footer__divider {
  width: 1px;
  height: 16px;
  background: #d7af6f;
}

.app-footer p {
  margin: 0;
}

@media (max-width: 768px) {
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