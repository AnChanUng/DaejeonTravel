<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

import kkumdoriImage from '@/assets/images/mascots/kkumdori.png'
import kkumsuniImage from '@/assets/images/mascots/kkumsuni.png'
import bakeryImage from '@/assets/images/backgrounds/bakery-left.png'
import daejeonRightImage from '@/assets/images/backgrounds/daejeon-right.png'

const router = useRouter()

const keyword = ref('')
const suggestions = ref([])
const searchError = ref('')
const searching = ref(false)
const suggestionLoading = ref(false)
const suggestionOpen = ref(false)

let debounceTimer = null

const routeNameMap = {
  '12': 'tourist-spot-detail',
  관광지: 'tourist-spot-detail',

  '32': 'accommodation-detail',
  숙박: 'accommodation-detail',

  '39': 'restaurant-detail',
  음식점: 'restaurant-detail'
}

const getContentType = (location) => {
  return String(
    location.content_type ??
    location.contentType ??
    location.contenttypeid ??
    location.type ??
    ''
  )
}

const getLocationId = (location) => {
  return (
    location.content_id ??
    location.contentId ??
    location.contentid ??
    location.id ??
    null
  )
}

const moveToDetail = async (location) => {
  const contentType = getContentType(location)
  const locationId = getLocationId(location)
  const routeName = routeNameMap[contentType]

  if (!routeName) {
    searchError.value = '지원하지 않는 장소 유형입니다.'
    console.error('알 수 없는 장소 유형:', location)
    return
  }

  if (!locationId) {
    searchError.value = '장소 상세 정보를 확인할 수 없습니다.'
    console.error('장소 ID가 없습니다:', location)
    return
  }

  suggestionOpen.value = false
  suggestions.value = []

  await router.push({
    name: routeName,
    params: {
      id: String(locationId)
    }
  })
}

const handleSearch = async () => {
  const value = keyword.value.trim()

  if (!value) {
    searchError.value = '장소 이름을 입력해주세요.'
    return
  }

  if (searching.value) {
    return
  }

  searching.value = true
  searchError.value = ''
  suggestionOpen.value = false

  try {
    const response = await api.get('/api/locations/exact', {
      params: {
        keyword: value
      }
    })
    await moveToDetail(response.data)
  } catch (error) {
    if (error.response?.status === 404) {
    } else {
      searchError.value = '검색 중 오류가 발생했습니다.'
      console.error('장소 정확 검색 실패:', error)
    }
  } finally {
    searching.value = false
  }
}

const selectSuggestion = async (location) => {
  keyword.value = location.title ?? location.name ?? ''
  searchError.value = ''

  await moveToDetail(location)
}

const closeSuggestions = () => {
  window.setTimeout(() => {
    suggestionOpen.value = false
  }, 150)
}

const openSuggestions = () => {
  if (keyword.value.trim()) {
    suggestionOpen.value = true
  }
}

watch(keyword, (newKeyword) => {
  window.clearTimeout(debounceTimer)

  searchError.value = ''

  const value = newKeyword.trim()

  if (!value) {
    suggestions.value = []
    suggestionOpen.value = false
    suggestionLoading.value = false
    return
  }

  debounceTimer = window.setTimeout(async () => {
    suggestionLoading.value = true

    try {
      const response = await api.get('/api/locations/suggestions', {
        params: {
          keyword: value,
          limit: 5
        }
      })

      suggestions.value = response.data.items ?? []
      suggestionOpen.value = true
    } catch (error) {
      suggestions.value = []
      suggestionOpen.value = false

      console.error('검색어 추천 조회 실패:', error)
    } finally {
      suggestionLoading.value = false
    }
  }, 300)
})

onUnmounted(() => {
  window.clearTimeout(debounceTimer)
})
</script>

<template>
  <section class="hero-section">
    <div class="hero-section__inner">
      <div
        class="hero-section__bakery"
        :style="{
          backgroundImage: `url(${bakeryImage})`
        }"
      />

      <div class="hero-section__pattern" />

      <img
        :src="kkumdoriImage"
        alt="꿈돌이"
        class="hero-section__mascot hero-section__mascot--left"
      />

      <div class="hero-section__content">
        <span class="hero-section__bread">
          🥐
        </span>

        <h1>
          대전의 맛과 여행을 한눈에
        </h1>

        <p>
          관광지, 음식점, 숙박 정보를 쉽고 빠르게 찾아보세요!
        </p>

        <div class="hero-section__search-wrapper">
          <form
            class="hero-section__search"
            @submit.prevent="handleSearch"
          >
            <input
              v-model="keyword"
              type="search"
              autocomplete="off"
              placeholder="장소 이름을 검색해보세요. 예: 한밭수목원, 유성온천"
              aria-label="장소 이름 검색"
              @focus="openSuggestions"
              @blur="closeSuggestions"
            />

            <button
              type="submit"
              :disabled="searching"
              aria-label="검색"
            >
              {{ searching ? '⋯' : '🔍' }}
            </button>
          </form>

          <div
            v-if="suggestionOpen"
            class="hero-section__suggestions"
          >
            <div
              v-if="suggestionLoading"
              class="hero-section__suggestion-state"
            >
              검색 중...
            </div>

            <template v-else>
              <button
                v-for="location in suggestions"
                :key="`${getContentType(location)}-${getLocationId(location)}`"
                type="button"
                class="hero-section__suggestion"
                @mousedown.prevent="selectSuggestion(location)"
              >
                <span class="hero-section__suggestion-icon">
                  🔍
                </span>

                <span class="hero-section__suggestion-info">
                  <strong>
                    {{ location.title ?? location.name }}
                  </strong>

                  <small v-if="location.addr ?? location.address">
                    {{ location.addr ?? location.address }}
                  </small>
                </span>
              </button>

              <div
                v-if="suggestions.length === 0"
                class="hero-section__suggestion-state"
              >
                검색 결과가 없습니다.
              </div>
            </template>
          </div>

          <p
            v-if="searchError"
            class="hero-section__search-error"
          >
            {{ searchError }}
          </p>
        </div>
      </div>

      <img
        :src="kkumsuniImage"
        alt="꿈순이"
        class="hero-section__mascot hero-section__mascot--right"
      />

      <img
        :src="daejeonRightImage"
        alt="Daejeon is U"
        class="hero-section__daejeon"
      />
    </div>
  </section>
</template>

<style scoped>
.hero-section {
  position: relative;
  width: 100%;
  height: 430px;
  overflow: visible;
}

.hero-section__inner {
  position: relative;
  width: 1600px;
  height: 430px;
  margin: 0 auto;
}

.hero-section__bakery {
  position: absolute;
  top: 0;
  left: 0;
  width: 504px;
  height: 408px;
  background-repeat: no-repeat;
  background-position: left top;
  background-size: contain;
  opacity: 0.4;
  z-index: 1;
}

.hero-section__daejeon {
  position: absolute;
  top: 0;
  right: 0;
  width: 433px;
  height: 449px;
  object-fit: contain;
  opacity: 0.3;
  filter: brightness(1.1) saturate(65%);
  z-index: 1;
}

.hero-section__pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(
      90deg,
      rgba(230, 169, 78, 0.08) 1px,
      transparent 1px
    ),
    linear-gradient(
      rgba(230, 169, 78, 0.08) 1px,
      transparent 1px
    );
  background-size: 120px 120px;
}

.hero-section__mascot {
  position: absolute;
  bottom: 30px;
  width: 240px;
  z-index: 5;
}

.hero-section__mascot--left {
  left: 300px;
}

.hero-section__mascot--right {
  right: 300px;
}

.hero-section__content {
  position: absolute;
  top: 70px;
  left: 50%;
  width: 670px;
  text-align: center;
  transform: translateX(-50%);
  z-index: 20;
}

.hero-section__bread {
  display: block;
  font-size: 32px;
}

.hero-section h1 {
  margin-top: 5px;
  color: #4b2b16;
  font-size: 56px;
  font-weight: 800;
  letter-spacing: -0.05em;
}

.hero-section p {
  margin-top: 10px;
  color: #76553a;
  font-size: 17px;
}

.hero-section__search-wrapper {
  position: relative;
  width: 100%;
  margin-top: 20px;
}

.hero-section__search {
  position: relative;
  width: 100%;
  height: 65px;
  padding: 7px 8px 7px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-sizing: border-box;
  background: #ffffff;
  border: 1px solid #d7af6f;
  border-radius: 999px;
  box-shadow: 0 10px 25px rgba(91, 57, 21, 0.15);
  z-index: 2;
}

.hero-section__search:focus-within {
  border-color: #e8a52a;
  box-shadow: 0 10px 28px rgba(91, 57, 21, 0.2);
}

.hero-section__search input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  font-size: 15px;
}

.hero-section__search input::-webkit-search-cancel-button {
  cursor: pointer;
}

.hero-section__search button {
  flex-shrink: 0;
  width: 51px;
  height: 51px;
  border: 0;
  border-radius: 50%;
  background: #f5bd45;
  cursor: pointer;
}

.hero-section__search button:disabled {
  cursor: default;
  opacity: 0.65;
}

.hero-section__suggestions {
  position: absolute;
  top: calc(100% + 8px);
  right: 12px;
  left: 12px;
  max-height: 260px;
  padding: 8px;
  overflow-y: auto;
  background: #fffdf8;
  border: 1px solid #e8c98c;
  border-radius: 16px;
  box-shadow: 0 15px 35px rgba(91, 57, 21, 0.18);
  text-align: left;
  z-index: 30;
}

.hero-section__suggestion {
  width: 100%;
  padding: 11px 12px;
  display: flex;
  align-items: center;
  gap: 11px;
  background: transparent;
  border: 0;
  border-radius: 10px;
  color: #5b3518;
  text-align: left;
  cursor: pointer;
}

.hero-section__suggestion:hover {
  background: #fff1cf;
}

.hero-section__suggestion-icon {
  flex-shrink: 0;
  font-size: 15px;
}

.hero-section__suggestion-info {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.hero-section__suggestion-info strong {
  overflow: hidden;
  font-size: 14px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hero-section__suggestion-info small {
  overflow: hidden;
  color: #8a6234;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hero-section__suggestion-state {
  padding: 18px 12px;
  color: #806040;
  font-size: 13px;
  text-align: center;
}

.hero-section__search-error {
  position: absolute;
  top: calc(100% + 9px);
  left: 20px;
  margin: 0;
  color: #c65353;
  font-size: 13px;
  text-align: left;
}

@media (max-width: 1600px) {
  .hero-section__inner {
    transform: scale(calc(100vw / 1600));
    transform-origin: top center;
  }
}

@media (max-width: 900px) {
  .hero-section__inner {
    width: 100%;
    transform: none;
  }

  .hero-section__bakery,
  .hero-section__daejeon {
    display: none;
  }

  .hero-section__mascot {
    opacity: 0.3;
  }

  .hero-section__content {
    width: min(670px, calc(100% - 32px));
  }

  .hero-section h1 {
    font-size: clamp(36px, 8vw, 56px);
  }
}
</style>