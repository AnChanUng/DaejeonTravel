<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import NotificationBell from './NotificationBell.vue'

const { locale } = useI18n()

const languageMenuOpen = ref(false)

const currentLanguage = ref(
  locale.value.toUpperCase()
)


const languages = [
  {
    code: 'KO',
    label: '한국어'
  },
  {
    code: 'EN',
    label: 'English'
  }
]


const toggleLanguageMenu = () => {
  languageMenuOpen.value = !languageMenuOpen.value
}


const selectLanguage = (languageCode) => {

  currentLanguage.value = languageCode

  // 실제 언어 변경
  locale.value = languageCode.toLowerCase()

  // 새로고침 후 유지
  localStorage.setItem(
    'language',
    languageCode.toLowerCase()
  )

  languageMenuOpen.value = false
}

</script>

<template>
  <header class="app-header">
    <div class="app-header__inner">
      <nav class="app-header__navigation">
        <RouterLink
          to="/"
          exact-active-class="app-header__link--active"
        >
          {{ $t('home') }}
        </RouterLink>

        <RouterLink
          to="/tourist-spots"
          active-class="app-header__link--active"
        >
          {{ $t('tourist') }}
        </RouterLink>

        <RouterLink
          to="/restaurants"
          active-class="app-header__link--active"
        >
          {{ $t('restaurant') }}
        </RouterLink>

        <RouterLink
          to="/accommodations"
          active-class="app-header__link--active"
        >
          {{ $t('accommodation') }}
        </RouterLink>

        <RouterLink
          to="/festivals"
          active-class="app-header__link--active"
        >
          {{ $t('festival') }}
        </RouterLink>

        <RouterLink
          to="/community"
          active-class="app-header__link--active"
        >
          {{ $t('community') }}
        </RouterLink>

        <RouterLink
          to="/map"
          active-class="app-header__link--active"
        >
          여행 지도
        </RouterLink>

        <RouterLink
          to="/dashboard"
          active-class="app-header__link--active"
        >
          대시보드
        </RouterLink>
      </nav>

      <!-- 오른쪽 영역: 알림 종 + 언어 선택 -->
      <div class="app-header__actions">
        <NotificationBell />

        <div class="app-header__language">
          <button
            type="button"
            class="app-header__language-button"
            :aria-expanded="languageMenuOpen"
            @click="toggleLanguageMenu"
          >
            <span
              class="app-header__language-icon"
              aria-hidden="true"
            >
              🌐
            </span>

            <span>
              {{ currentLanguage }}
            </span>

            <span
              class="app-header__language-arrow"
              aria-hidden="true"
            >
              ▾
            </span>
          </button>

          <div
            v-if="languageMenuOpen"
            class="app-header__language-menu"
          >
            <button
              v-for="language in languages"
              :key="language.code"
              type="button"
              :class="{
                'app-header__language-option--active':
                  currentLanguage === language.code
              }"
              @click="selectLanguage(language.code)"
            >
              <span>
                {{ language.code }}
              </span>

              <span>
                {{ language.label }}
              </span>
            </button>
          </div>
        </div>
      </div>

      <button
        type="button"
        class="app-header__mobile-menu"
        :aria-label="$t('openMenu')"
      >
        ☰
      </button>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: relative;
  z-index: 50;
  padding: 35px 5% 0;
}

.app-header__inner {
  position: relative;
  width: min(1420px, 100%);
  min-height: 88px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  background: rgba(255, 253, 247, 0.96);
  border: 1px solid var(--color-border);
  border-radius: 18px;
  box-shadow: var(--shadow-medium);
  backdrop-filter: blur(10px);
}

/* 메뉴가 8개로 늘어나 언어 버튼과 겹치지 않도록 간격을 조금 줄임 */
.app-header__navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(20px, 2.4vw, 42px);
}

.app-header__navigation a {
  position: relative;
  padding: 28px 0;
  color: var(--color-brown-900);
  font-size: 18px;
  font-weight: 700;
  white-space: nowrap;
  text-decoration: none;
  transition: color 0.2s ease;
}

.app-header__navigation a::after {
  position: absolute;
  right: 0;
  bottom: 18px;
  left: 0;
  height: 2px;
  background: var(--color-gold-500);
  content: '';
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 0.2s ease;
}

.app-header__navigation a:hover {
  color: var(--color-gold-500);
}

.app-header__navigation a:hover::after,
.app-header__navigation a.app-header__link--active::after {
  transform: scaleX(1);
}

.app-header__navigation a.app-header__link--active {
  color: var(--color-gold-500);
  font-weight: 800;
}

/* 알림 종 + 언어 선택을 나란히 배치 */
.app-header__actions {
  position: absolute;
  top: 50%;
  right: 32px;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 언어 드롭다운의 기준점 역할만 담당 */
.app-header__language {
  position: relative;
}

.app-header__language-button {
  min-width: 94px;
  padding: 9px 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  background: #fffaf0;
  border: 1px solid #ddc49e;
  border-radius: 999px;
  color: var(--color-brown-800);
  cursor: pointer;
}

.app-header__language-button:hover {
  background: #fff2d7;
}

.app-header__language-icon {
  font-size: 15px;
}

.app-header__language-arrow {
  font-size: 12px;
}

.app-header__language-menu {
  position: absolute;
  top: calc(100% + 9px);
  right: 0;
  width: 145px;
  padding: 7px;
  background: #fffdf8;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  box-shadow: var(--shadow-small);
}

.app-header__language-menu button {
  width: 100%;
  padding: 10px;
  display: grid;
  grid-template-columns: 30px 1fr;
  gap: 8px;
  background: transparent;
  border: 0;
  border-radius: 8px;
  text-align: left;
  cursor: pointer;
}

.app-header__language-menu button:hover,
.app-header__language-option--active {
  background: #fff0d1 !important;
}

.app-header__mobile-menu {
  display: none;
  background: transparent;
  border: 0;
  font-size: 27px;
  color: var(--color-brown-900);
  cursor: pointer;
}

@media (max-width: 1250px) {
  .app-header__navigation {
    gap: 20px;
  }

  .app-header__navigation a {
    font-size: 15px;
  }
}

@media (max-width: 900px) {
  .app-header__navigation {
    display: none;
  }

  .app-header__mobile-menu {
    display: block;
  }

  .app-header__inner {
    justify-content: flex-start;
    padding: 0 20px;
  }
}

@media (max-width: 520px) {
  .app-header {
    padding: 12px 12px 0;
  }

  .app-header__inner {
    min-height: 66px;
  }

  .app-header__actions {
    right: 16px;
    gap: 6px;
  }

  .app-header__language-button {
    min-width: auto;
  }

  .app-header__language-icon {
    display: none;
  }
}
</style>