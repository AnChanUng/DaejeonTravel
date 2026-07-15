<script setup>
import { ref } from 'vue'

const languageMenuOpen = ref(false)
const currentLanguage = ref('KO')

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
          홈
        </RouterLink>

        <RouterLink
          to="/tourist-spots"
          active-class="app-header__link--active"
        >
          관광지
        </RouterLink>

        <RouterLink
          to="/restaurants"
          active-class="app-header__link--active"
        >
          음식점
        </RouterLink>

        <RouterLink
          to="/accommodations"
          active-class="app-header__link--active"
        >
          숙박
        </RouterLink>

        <RouterLink
          to="/festivals"
          active-class="app-header__link--active"
        >
          축제 캘린더
        </RouterLink>

        <RouterLink
          to="/community"
          active-class="app-header__link--active"
        >
          커뮤니티
        </RouterLink>
      </nav>

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

      <button
        type="button"
        class="app-header__mobile-menu"
        aria-label="메뉴 열기"
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

.app-header__navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(24px, 3vw, 52px);
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

.app-header__language {
  position: absolute;
  top: 50%;
  right: 32px;
  transform: translateY(-50%);
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

@media (max-width: 1150px) {
  .app-header__navigation {
    gap: 22px;
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

  .app-header__language {
    right: 16px;
  }

  .app-header__language-button {
    min-width: auto;
  }

  .app-header__language-icon {
    display: none;
  }
}
</style>