<script setup>
import { ref, computed, onMounted } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import api from '../api'
import PageLayout from '../components/layout/PageLayout.vue'

// 지역별 이벤트 색 (따뜻한 팔레트 유지)
const REGION_COLORS = {
  대전: '#e8a52a',
  세종: '#d97f5f',
  충남: '#7fa06b',
  충북: '#a67fb5',
  기타: '#b99b74',
}

const regions = ['전체', '대전', '세종', '충남', '충북']
const activeRegion = ref('')

const events = ref([])
const undated = ref([])
const loading = ref(true)

const selected = ref(null) // 모달에 띄울 축제

// 지역 필터 적용된 이벤트
const filteredEvents = computed(() =>
  activeRegion.value
    ? events.value.filter((e) => e.region === activeRegion.value)
    : events.value
)

const filteredUndated = computed(() =>
  activeRegion.value
    ? undated.value.filter((e) => e.region === activeRegion.value)
    : undated.value
)

// FullCalendar 이벤트 형식으로 변환
// (FullCalendar의 end는 '해당 날짜 미포함'이라 하루 더해준다)
function addOneDay(dateStr) {
  const d = new Date(dateStr)
  d.setDate(d.getDate() + 1)
  return d.toISOString().slice(0, 10)
}

const calendarEvents = computed(() =>
  filteredEvents.value.map((f) => ({
    id: f.content_id,
    title: f.title,
    start: f.start,
    end: addOneDay(f.end),
    display: 'block',
    backgroundColor: REGION_COLORS[f.region],
    borderColor: REGION_COLORS[f.region],
    extendedProps: f,
  }))
)

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
  headerToolbar: {
    left: 'prev',
    center: 'title',
    right: 'next today',
  },
  events: calendarEvents.value,
  dayMaxEvents: 3,
  height: 'auto',
  eventClick(info) {
    selected.value = info.event.extendedProps
  },
}))

function selectRegion(r) {
  activeRegion.value = r === '전체' ? '' : r
}

function formatPeriod(f) {
  if (!f.start) return '일정 확인 중'
  return f.start === f.end ? f.start : `${f.start} ~ ${f.end}`
}

const kakaoMapUrl = computed(() => {
  if (!selected.value?.lat || !selected.value?.lng) return null
  const name = encodeURIComponent(selected.value.title)
  return `https://map.kakao.com/link/map/${name},${selected.value.lat},${selected.value.lng}`
})

onMounted(async () => {
  try {
    const res = await api.get('/api/festivals')
    events.value = res.data.events
    undated.value = res.data.undated
  } catch {
    events.value = []
    undated.value = []
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <PageLayout>

    <!-- 페이지 헤드 -->
    <div class="fest-head">
      <span class="fest-head__emoji">🎪</span>
      <h1>축제 캘린더</h1>
      <p>대전·충청 권역의 축제 일정을 한눈에 확인하세요</p>
    </div>

    <!-- 지역 필터 (색 범례 겸용) -->
    <div class="region-tabs">
      <button
        v-for="r in regions"
        :key="r"
        :class="{ active: (r === '전체' && !activeRegion) || r === activeRegion }"
        @click="selectRegion(r)"
      >
        <span
          v-if="r !== '전체'"
          class="dot"
          :style="{ background: REGION_COLORS[r] }"
        ></span>
        {{ r }}
      </button>
    </div>

    <!-- 캘린더 -->
    <div v-if="loading" class="state-box">불러오는 중...</div>

    <template v-else>
      <div class="calendar-card">
        <FullCalendar :options="calendarOptions" />
      </div>

      <!-- 일정 미입력 축제 -->
      <div v-if="filteredUndated.length" class="undated">
        <h2>🗓️ 일정 확인 중인 축제</h2>
        <p class="undated__sub">정확한 일정이 확정되면 캘린더에 표시돼요</p>

        <div class="undated__grid">
          <button
            v-for="f in filteredUndated"
            :key="f.content_id"
            class="undated__card"
            @click="selected = f"
          >
            <span class="dot" :style="{ background: REGION_COLORS[f.region] }"></span>
            <span class="undated__title">{{ f.title }}</span>
            <span class="undated__region">{{ f.region }}</span>
          </button>
        </div>
      </div>
    </template>

    <!-- 축제 상세 모달 -->
    <div v-if="selected" class="modal-bg" @click.self="selected = null">
      <div class="modal">
        <button class="modal__close" @click="selected = null">×</button>

        <div class="modal__hero">
          <img v-if="selected.image" :src="selected.image" :alt="selected.title" />
          <div v-else class="modal__placeholder">🎪</div>
        </div>

        <div class="modal__body">
          <div class="badges">
            <span
              class="badge"
              :style="{
                background: REGION_COLORS[selected.region] + '22',
                borderColor: REGION_COLORS[selected.region],
              }"
            >
              📍 {{ selected.region }}
            </span>
            <span class="badge badge--period">{{ formatPeriod(selected) }}</span>
          </div>

          <h2>{{ selected.title }}</h2>

          <div class="info-list">
            <div class="info-row">
              <span class="info-row__label">장소</span>
              <span>{{ selected.addr || '장소 정보가 제공되지 않았어요' }}</span>
            </div>
            <div class="info-row" v-if="selected.tel">
              <span class="info-row__label">문의</span>
              <a :href="`tel:${selected.tel}`" class="link">{{ selected.tel }}</a>
            </div>
          </div>

          <a
            v-if="kakaoMapUrl"
            :href="kakaoMapUrl"
            target="_blank"
            rel="noopener"
            class="map-btn"
          >
            🗺️ 카카오맵에서 위치 보기
          </a>
        </div>
      </div>
    </div>

  </PageLayout>
</template>

<style scoped>
/* 페이지 헤드 */
.fest-head {
  text-align: center;
  margin-bottom: 26px;
}

.fest-head__emoji {
  font-size: 30px;
}

.fest-head h1 {
  margin-top: 4px;
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.05em;
  color: var(--color-brown-900);
}

.fest-head p {
  margin-top: 8px;
  font-size: 15px;
  color: var(--color-brown-500);
}

/* 지역 필터 칩 (범례 겸용) */
.region-tabs {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 22px;
}

.region-tabs button {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 18px;
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

.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* 캘린더 카드 + FullCalendar 테마 커스텀 */
.calendar-card {
  padding: 22px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 22px;
  box-shadow: var(--shadow-small);
}

.calendar-card :deep(.fc) {
  --fc-border-color: #f0deba;
  --fc-today-bg-color: #fff1d6;
  --fc-page-bg-color: transparent;
  font-size: 14px;
}

.calendar-card :deep(.fc-toolbar-title) {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--color-brown-900);
}

.calendar-card :deep(.fc-button) {
  background: var(--color-cream-300);
  border: 1.5px solid #e8cfaa;
  border-radius: 999px;
  color: var(--color-brown-800);
  font-weight: 700;
  padding: 6px 14px;
  box-shadow: none !important;
}

.calendar-card :deep(.fc-button:hover) {
  background: var(--color-gold-300);
  border-color: var(--color-gold-500);
  color: var(--color-brown-900);
}

.calendar-card :deep(.fc-button-active),
.calendar-card :deep(.fc-button:disabled) {
  background: var(--color-gold-400) !important;
  border-color: var(--color-gold-500) !important;
  color: var(--color-brown-900) !important;
  opacity: 1;
}

.calendar-card :deep(.fc-col-header-cell-cushion) {
  padding: 10px 0;
  color: var(--color-brown-700);
  font-weight: 700;
  text-decoration: none;
}

.calendar-card :deep(.fc-daygrid-day-number) {
  color: var(--color-brown-800);
  font-weight: 600;
  text-decoration: none;
}

.calendar-card :deep(.fc-day-sun .fc-daygrid-day-number) {
  color: #c0392b;
}

.calendar-card :deep(.fc-event) {
  border-radius: 8px;
  padding: 2px 6px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  border: 0;
}

.calendar-card :deep(.fc-event-title) {
  color: #fffdf8;
}

.calendar-card :deep(.fc-more-link) {
  color: var(--color-brown-700);
  font-weight: 700;
}

/* 일정 미입력 축제 */
.undated {
  margin-top: 34px;
}

.undated h2 {
  font-size: 20px;
  font-weight: 800;
  color: var(--color-brown-900);
}

.undated__sub {
  margin: 6px 0 16px;
  font-size: 13px;
  color: var(--color-brown-500);
}

.undated__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.undated__card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 16px;
  box-shadow: var(--shadow-small);
  cursor: pointer;
  text-align: left;
  transition: transform 0.15s ease;
}

.undated__card:hover {
  transform: translateY(-2px);
}

.undated__title {
  flex: 1;
  font-size: 14px;
  font-weight: 700;
  color: var(--color-brown-900);
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.undated__region {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-brown-500);
}

/* 상태 박스 */
.state-box {
  padding: 70px 0;
  text-align: center;
  background: var(--color-cream-100);
  border: 1px dashed #dbb87e;
  border-radius: 18px;
  color: var(--color-brown-500);
  font-weight: 700;
}

/* 모달 */
.modal-bg {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(63, 40, 25, 0.45);
}

.modal {
  position: relative;
  width: min(460px, 100%);
  max-height: 88vh;
  overflow-y: auto;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 22px;
  box-shadow: var(--shadow-medium);
}

.modal__close {
  position: absolute;
  top: 12px;
  right: 14px;
  z-index: 2;
  width: 34px;
  height: 34px;
  background: rgba(255, 253, 248, 0.92);
  border: 1px solid #e5c085;
  border-radius: 50%;
  color: var(--color-brown-800);
  font-size: 20px;
  cursor: pointer;
}

.modal__hero {
  height: 210px;
  background: var(--color-cream-300);
}

.modal__hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal__placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 52px;
  background-image:
    linear-gradient(90deg, rgba(230, 169, 78, 0.12) 1px, transparent 1px),
    linear-gradient(rgba(230, 169, 78, 0.12) 1px, transparent 1px);
  background-size: 32px 32px;
}

.modal__body {
  padding: 22px 24px 26px;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.badge {
  padding: 4px 12px;
  background: var(--color-cream-300);
  border: 1px solid #e5c085;
  border-radius: 999px;
  color: var(--color-brown-800);
  font-size: 13px;
  font-weight: 700;
}

.badge--period {
  background: var(--color-gold-300);
  border-color: var(--color-gold-500);
  color: var(--color-brown-900);
}

.modal h2 {
  font-size: 21px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--color-brown-900);
}

.info-list {
  margin-top: 14px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #fffaf0;
  border: 1px solid #f0deba;
  border-radius: 14px;
  font-size: 14px;
  color: var(--color-brown-800);
}

.info-row {
  display: flex;
  gap: 12px;
  line-height: 1.6;
}

.info-row__label {
  flex-shrink: 0;
  width: 34px;
  font-weight: 700;
  color: var(--color-brown-500);
}

.link {
  color: var(--color-brown-800);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.map-btn {
  display: inline-block;
  margin-top: 16px;
  padding: 12px 22px;
  background: var(--color-gold-400);
  border-radius: 999px;
  box-shadow: 0 6px 16px rgba(232, 165, 42, 0.3);
  color: var(--color-brown-900);
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
}

.map-btn:hover {
  background: var(--color-gold-500);
}

@media (max-width: 640px) {
  .fest-head h1 {
    font-size: 28px;
  }

  .undated__grid {
    grid-template-columns: 1fr;
  }

  .calendar-card {
    padding: 12px;
  }

  .calendar-card :deep(.fc-toolbar-title) {
    font-size: 17px;
  }
}
</style>