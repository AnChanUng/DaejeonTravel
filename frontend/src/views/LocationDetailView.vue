<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'

const route = useRoute()
const router = useRouter()
const item = ref(null)
const notFound = ref(false)

const TYPE_META = {
  관광지: { emoji: '🏞️', listPath: '/tourist-spots' },
  음식점: { emoji: '🍜', listPath: '/restaurants' },
  숙박: { emoji: '🛏️', listPath: '/accommodations' },
}

const typeMeta = computed(
  () => TYPE_META[item.value?.content_type] || TYPE_META['관광지']
)

function district(addr) {
  if (!addr) return ''
  const parts = addr.split(' ')
  return parts.length >= 2 ? parts[1] : parts[0]
}

// 카카오맵 길찾기 링크 (좌표 기반, API 키 불필요)
const kakaoMapUrl = computed(() => {
  if (!item.value?.lat || !item.value?.lng) return null
  const name = encodeURIComponent(item.value.title)
  return `https://map.kakao.com/link/map/${name},${item.value.lat},${item.value.lng}`
})

async function fetchItem() {
  try {
    const res = await api.get(`/api/locations/${route.params.id}`)
    item.value = res.data
  } catch {
    notFound.value = true
  }
}

onMounted(fetchItem)
</script>

<template>
  <PageLayout>

    <button class="back" @click="router.back()">‹ 목록으로</button>

    <div v-if="notFound" class="state-box">
      <p>장소를 찾을 수 없어요</p>
      <BaseButton @click="router.push('/')">메인으로 돌아가기</BaseButton>
    </div>

    <template v-else-if="item">
      <div class="detail-card">

        <!-- 대표 이미지 -->
        <div class="detail-card__hero">
          <img
            v-if="item.image"
            :src="item.image"
            :alt="item.title"
          />
          <div v-else class="detail-card__placeholder">
            <span>{{ typeMeta.emoji }}</span>
            <p>사진 준비 중</p>
          </div>
        </div>

        <div class="detail-card__body">
          <div class="badges">
            <span class="badge badge--type">{{ typeMeta.emoji }} {{ item.content_type }}</span>
            <span v-if="district(item.addr)" class="badge">📍 {{ district(item.addr) }}</span>
          </div>

          <h1>{{ item.title }}</h1>

          <div class="info-list">
            <div class="info-row">
              <span class="info-row__label">주소</span>
              <span class="info-row__value">{{ item.addr || '주소 정보가 제공되지 않았어요' }}</span>
            </div>
            <div class="info-row" v-if="item.tel">
              <span class="info-row__label">전화</span>
              <a class="info-row__value link" :href="`tel:${item.tel}`">{{ item.tel }}</a>
            </div>
          </div>

          <div class="btn-row" v-if="kakaoMapUrl">
            <a :href="kakaoMapUrl" target="_blank" rel="noopener" class="map-btn">
              🗺️ 카카오맵에서 위치 보기
            </a>
          </div>
        </div>

      </div>
    </template>

  </PageLayout>
</template>

<style scoped>
.back {
  margin-bottom: 14px;
  padding: 6px 0;
  background: none;
  border: 0;
  color: var(--color-brown-500);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.back:hover {
  color: var(--color-brown-800);
}

.detail-card {
  overflow: hidden;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 22px;
  box-shadow: var(--shadow-small);
}

.detail-card__hero {
  height: 340px;
  background: var(--color-cream-300);
}

.detail-card__hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-card__placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 100%;
  background-image:
    linear-gradient(90deg, rgba(230, 169, 78, 0.12) 1px, transparent 1px),
    linear-gradient(rgba(230, 169, 78, 0.12) 1px, transparent 1px);
  background-size: 36px 36px;
}

.detail-card__placeholder span {
  font-size: 52px;
  opacity: 0.75;
}

.detail-card__placeholder p {
  font-size: 13px;
  font-weight: 700;
  color: #b99b74;
}

.detail-card__body {
  padding: 28px 32px 32px;
}

.badges {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.badge {
  padding: 4px 12px;
  background: var(--color-cream-300);
  border: 1px solid #e5c085;
  border-radius: 999px;
  color: var(--color-brown-700);
  font-size: 13px;
  font-weight: 700;
}

.badge--type {
  background: var(--color-gold-300);
  border-color: var(--color-gold-500);
  color: var(--color-brown-900);
}

h1 {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--color-brown-900);
}

.info-list {
  margin-top: 20px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #fffaf0;
  border: 1px solid #f0deba;
  border-radius: 16px;
}

.info-row {
  display: flex;
  gap: 14px;
  font-size: 15px;
  line-height: 1.6;
}

.info-row__label {
  flex-shrink: 0;
  width: 40px;
  font-weight: 700;
  color: var(--color-brown-500);
}

.info-row__value {
  color: var(--color-brown-800);
}

.info-row__value.link {
  color: var(--color-brown-800);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.btn-row {
  margin-top: 22px;
}

.map-btn {
  display: inline-block;
  padding: 13px 26px;
  background: var(--color-gold-400);
  border-radius: 999px;
  box-shadow: 0 6px 16px rgba(232, 165, 42, 0.3);
  color: var(--color-brown-900);
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.15s ease;
}

.map-btn:hover {
  background: var(--color-gold-500);
}

.state-box {
  padding: 70px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background: var(--color-cream-100);
  border: 1px dashed #dbb87e;
  border-radius: 18px;
  color: var(--color-brown-500);
}

@media (max-width: 600px) {
  .detail-card__hero {
    height: 220px;
  }

  .detail-card__body {
    padding: 20px;
  }

  h1 {
    font-size: 22px;
  }
}
</style>