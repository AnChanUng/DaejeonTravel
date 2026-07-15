<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import PageLayout from '../components/layout/PageLayout.vue'

const props = defineProps({
  type: {
    type: String,
    required: true, // '관광지' | '음식점' | '숙박'
  },
})

const router = useRouter()

// 타입별 페이지 문구
const META = {
  관광지: {
    emoji: '🏞️',
    title: '대전·충청 관광지',
    sub: '가볼 만한 곳을 한눈에 둘러보세요',
    detailBase: '/tourist-spots',
  },
  음식점: {
    emoji: '🍜',
    title: '대전·충청의 맛집',
    sub: '현지인이 사랑하는 음식점을 만나보세요',
    detailBase: '/restaurants',
  },
  숙박: {
    emoji: '🛏️',
    title: '대전·충청 숙박',
    sub: '편안한 하룻밤을 보낼 곳을 찾아보세요',
    detailBase: '/accommodations',
  },
}

const pageMeta = computed(() => META[props.type] || META['관광지'])

const regions = ['전체', '대전', '세종', '충남', '충북']

const items = ref([])
const keyword = ref('')
const region = ref('')
const page = ref(1)
const size = 12
const total = ref(0)
const loading = ref(true)

const totalPages = computed(() => Math.ceil(total.value / size))

// 페이지네이션 번호 (최대 5개만 노출)
const pageNumbers = computed(() => {
  const start = Math.max(1, Math.min(page.value - 2, totalPages.value - 4))
  const end = Math.min(totalPages.value, start + 4)
  const nums = []
  for (let i = start; i <= end; i++) nums.push(i)
  return nums
})

async function fetchItems() {
  loading.value = true
  try {
    const res = await api.get('/api/locations', {
      params: {
        type: props.type,
        region: region.value || undefined,
        keyword: keyword.value || undefined,
        page: page.value,
        size,
      },
    })
    items.value = res.data.items
    total.value = res.data.total
  } catch {
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function search() {
  page.value = 1
  fetchItems()
}

function selectRegion(r) {
  region.value = r === '전체' ? '' : r
  page.value = 1
  fetchItems()
}

function movePage(p) {
  page.value = p
  fetchItems()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function goDetail(contentId) {
  router.push(`${pageMeta.value.detailBase}/${contentId}`)
}

// 주소에서 시군구 추출: "대전광역시 서구 ..." → "서구"
function district(addr) {
  if (!addr) return ''
  const parts = addr.split(' ')
  return parts.length >= 2 ? parts[1] : parts[0]
}

// 관광지 ↔ 음식점 ↔ 숙박 전환 시 (같은 컴포넌트 재사용) 목록 초기화
watch(
  () => props.type,
  () => {
    keyword.value = ''
    region.value = ''
    page.value = 1
    fetchItems()
  }
)

onMounted(fetchItems)
</script>

<template>
  <PageLayout>

    <!-- 페이지 헤드 -->
    <div class="loc-head">
      <span class="loc-head__emoji">{{ pageMeta.emoji }}</span>
      <h1>{{ pageMeta.title }}</h1>
      <p>{{ pageMeta.sub }}</p>
    </div>

    <!-- 지역 필터 -->
    <div class="region-tabs">
      <button
        v-for="r in regions"
        :key="r"
        :class="{ active: (r === '전체' && !region) || r === region }"
        @click="selectRegion(r)"
      >
        {{ r }}
      </button>
    </div>

    <!-- 검색 -->
    <div class="search-box">
      <span class="search-box__icon">🔍</span>
      <input
        v-model="keyword"
        @keyup.enter="search"
        :placeholder="`${type} 이름으로 검색해보세요`"
      />
      <button class="search-box__btn" @click="search">검색</button>
    </div>

    <p v-if="!loading" class="result-count">
      총 <strong>{{ total.toLocaleString() }}</strong>곳
    </p>

    <!-- 카드 그리드 -->
    <div v-if="loading" class="state-box">불러오는 중...</div>

    <div v-else-if="items.length" class="card-grid">
      <div
        v-for="item in items"
        :key="item.content_id"
        class="loc-card"
        @click="goDetail(item.content_id)"
      >
        <div class="loc-card__thumb">
          <img
            v-if="item.image"
            :src="item.image"
            :alt="item.title"
            loading="lazy"
          />
          <div v-else class="loc-card__placeholder">
            <span>{{ pageMeta.emoji }}</span>
            <p>사진 준비 중</p>
          </div>
          <span v-if="district(item.addr)" class="loc-card__badge">
            📍 {{ district(item.addr) }}
          </span>
        </div>

        <div class="loc-card__body">
          <h3>{{ item.title }}</h3>
          <p class="addr">{{ item.addr || '주소 정보 없음' }}</p>
          <p v-if="item.tel" class="tel">📞 {{ item.tel }}</p>
        </div>
      </div>
    </div>

    <div v-else class="state-box">
      <p>검색 결과가 없어요</p>
      <p class="state-box__sub">다른 지역이나 검색어로 찾아보세요</p>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page === 1" @click="movePage(page - 1)">‹</button>
      <button
        v-for="p in pageNumbers"
        :key="p"
        :class="{ active: p === page }"
        @click="movePage(p)"
      >
        {{ p }}
      </button>
      <button :disabled="page === totalPages" @click="movePage(page + 1)">›</button>
    </div>

  </PageLayout>
</template>

<style scoped>
/* 페이지 헤드 — 메인 히어로 카피와 같은 톤 */
.loc-head {
  text-align: center;
  margin-bottom: 28px;
}

.loc-head__emoji {
  font-size: 30px;
}

.loc-head h1 {
  margin-top: 4px;
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.05em;
  color: var(--color-brown-900);
}

.loc-head p {
  margin-top: 8px;
  font-size: 15px;
  color: var(--color-brown-500);
}

/* 지역 필터 칩 */
.region-tabs {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
}

.region-tabs button {
  padding: 8px 20px;
  background: var(--color-cream-100);
  border: 1.5px solid #e8cfaa;
  border-radius: 999px;
  color: var(--color-brown-700);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.region-tabs button:hover {
  background: var(--color-cream-300);
}

.region-tabs button.active {
  background: var(--color-gold-400);
  border-color: var(--color-gold-500);
  color: var(--color-brown-900);
}

/* 검색 — 메인 히어로 검색창과 같은 알약형 */
.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 560px;
  margin: 0 auto 10px;
  padding: 7px 8px 7px 20px;
  background: #fff;
  border: 1.5px solid #dbb87e;
  border-radius: 999px;
  box-shadow: 0 8px 20px rgba(91, 57, 21, 0.1);
}

.search-box__icon {
  font-size: 17px;
}

.search-box input {
  flex: 1;
  min-width: 0;
  padding: 9px 0;
  border: 0;
  outline: 0;
  background: transparent;
  font-size: 15px;
  color: var(--color-brown-900);
}

.search-box input::placeholder {
  color: #b99b74;
}

.search-box__btn {
  padding: 10px 20px;
  background: var(--color-gold-400);
  border: 0;
  border-radius: 999px;
  color: var(--color-brown-900);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.search-box__btn:hover {
  background: var(--color-gold-500);
}

.result-count {
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--color-brown-500);
  text-align: right;
}

.result-count strong {
  color: var(--color-brown-800);
}

/* 카드 그리드 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.loc-card {
  overflow: hidden;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 20px;
  box-shadow: var(--shadow-small);
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.loc-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-medium);
}

.loc-card__thumb {
  position: relative;
  height: 170px;
  overflow: hidden;
  background: var(--color-cream-300);
}

.loc-card__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.loc-card:hover .loc-card__thumb img {
  transform: scale(1.06);
}

/* 이미지 없는 장소용 플레이스홀더 — 메인 히어로의 골드 그리드 패턴 오마주 */
.loc-card__placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 100%;
  background-image:
    linear-gradient(90deg, rgba(230, 169, 78, 0.12) 1px, transparent 1px),
    linear-gradient(rgba(230, 169, 78, 0.12) 1px, transparent 1px);
  background-size: 28px 28px;
}

.loc-card__placeholder span {
  font-size: 34px;
  opacity: 0.75;
}

.loc-card__placeholder p {
  font-size: 12px;
  color: #b99b74;
  font-weight: 700;
}

.loc-card__badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 10px;
  background: rgba(255, 253, 248, 0.94);
  border: 1px solid #e5c085;
  border-radius: 999px;
  color: var(--color-brown-800);
  font-size: 12px;
  font-weight: 700;
}

.loc-card__body {
  padding: 14px 16px 16px;
}

.loc-card__body h3 {
  font-size: 16px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--color-brown-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.loc-card__body .addr {
  margin-top: 5px;
  font-size: 13px;
  line-height: 1.5;
  color: var(--color-brown-500);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.loc-card__body .tel {
  margin-top: 6px;
  font-size: 12px;
  color: var(--color-brown-700);
}

/* 빈 상태 / 로딩 */
.state-box {
  padding: 70px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  background: var(--color-cream-100);
  border: 1px dashed #dbb87e;
  border-radius: 18px;
  color: var(--color-brown-700);
  font-size: 15px;
  font-weight: 700;
}

.state-box__sub {
  font-size: 13px;
  font-weight: 400;
  color: var(--color-brown-500);
}

/* 페이지네이션 — 게시판과 동일 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 30px;
}

.pagination button {
  min-width: 38px;
  height: 38px;
  background: var(--color-cream-100);
  border: 1px solid #e8cfaa;
  border-radius: 12px;
  color: var(--color-brown-700);
  font-weight: 700;
  cursor: pointer;
}

.pagination button:hover:not(:disabled) {
  background: var(--color-cream-300);
}

.pagination button.active {
  background: var(--color-gold-400);
  border-color: var(--color-gold-500);
  color: var(--color-brown-900);
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: default;
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .loc-head h1 {
    font-size: 28px;
  }
}

@media (max-width: 480px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>