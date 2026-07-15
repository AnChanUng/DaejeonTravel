<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import api from '../api'
import PageLayout from '../components/layout/PageLayout.vue'

const router = useRouter()

const TYPE_META = {
  관광지: { color: '#e8a52a', detailBase: '/tourist-spots', emoji: '🏞️' },
  음식점: { color: '#d97f5f', detailBase: '/restaurants', emoji: '🍜' },
}

const types = ['전체', '관광지', '음식점']
const regions = ['전체', '대전', '세종', '충남', '충북']

const activeType = ref('전체')
const activeRegion = ref('')
const loading = ref(true)
const visibleCount = ref(0)

// 경로 안내 상태
const routeMode = ref(false)
const routeStops = ref([]) // {content_id, title, lat, lng, type}
const routeInfo = ref(null) // {distanceKm, durationMin, isStraight}
const routing = ref(false)

const mapEl = ref(null)
let map = null
let markerLayer = null
let routeLayer = null
const allItems = { 관광지: [], 음식점: [] }

async function fetchAll() {
  loading.value = true
  try {
    const [spots, foods] = await Promise.all([
      api.get('/api/locations/map', { params: { type: '관광지' } }),
      api.get('/api/locations/map', { params: { type: '음식점' } }),
    ])
    allItems['관광지'] = spots.data.items
    allItems['음식점'] = foods.data.items
  } finally {
    loading.value = false
  }
}

function visibleItems() {
  const typeList =
    activeType.value === '전체' ? ['관광지', '음식점'] : [activeType.value]
  const prefix = {
    대전: '대전',
    세종: '세종',
    충남: '충청남도',
    충북: '충청북도',
  }[activeRegion.value]

  const items = []
  for (const t of typeList) {
    for (const item of allItems[t]) {
      if (prefix && !(item.addr || '').startsWith(prefix)) continue
      items.push(item)
    }
  }
  return items
}

// 팝업을 DOM으로 만들어 버튼에 이벤트를 직접 연결
function buildPopup(item) {
  const meta = TYPE_META[item.content_type]
  const el = document.createElement('div')
  el.className = 'map-popup'
  el.innerHTML = `
    <p class="map-popup__type">${meta.emoji} ${item.content_type}</p>
    <p class="map-popup__title">${item.title}</p>
    <p class="map-popup__addr">${item.addr || ''}</p>
  `
  const btnRow = document.createElement('div')
  btnRow.className = 'map-popup__btns'

  const detailBtn = document.createElement('button')
  detailBtn.textContent = '상세보기'
  detailBtn.className = 'map-popup__btn'
  detailBtn.addEventListener('click', () =>
    router.push(`${meta.detailBase}/${item.content_id}`)
  )

  const routeBtn = document.createElement('button')
  routeBtn.textContent = '➕ 경로에 추가'
  routeBtn.className = 'map-popup__btn map-popup__btn--gold'
  routeBtn.addEventListener('click', () => addStop(item))

  btnRow.appendChild(detailBtn)
  btnRow.appendChild(routeBtn)
  el.appendChild(btnRow)
  return el
}

function renderMarkers() {
  markerLayer.clearLayers()
  const items = visibleItems()
  visibleCount.value = items.length

  for (const item of items) {
    const meta = TYPE_META[item.content_type]
    const marker = L.circleMarker([item.lat, item.lng], {
      radius: 7,
      color: '#fffdf8',
      weight: 1.5,
      fillColor: meta.color,
      fillOpacity: 0.9,
    })
    marker.bindPopup(() => buildPopup(item), { maxWidth: 240 })
    markerLayer.addLayer(marker)
  }
}

function selectType(t) {
  activeType.value = t
  renderMarkers()
}

function selectRegion(r) {
  activeRegion.value = r === '전체' ? '' : r
  renderMarkers()
}

// ------- 경로 안내 -------
function addStop(item) {
  if (routeStops.value.some((s) => s.content_id === item.content_id)) {
    alert('이미 경로에 추가된 장소예요')
    return
  }
  if (routeStops.value.length >= 8) {
    alert('경로는 최대 8곳까지 추가할 수 있어요')
    return
  }
  routeStops.value.push({
    content_id: item.content_id,
    title: item.title,
    lat: item.lat,
    lng: item.lng,
    type: item.content_type,
  })
  routeMode.value = true
  map.closePopup()
  drawRoute()
}

function removeStop(index) {
  routeStops.value.splice(index, 1)
  drawRoute()
}

function clearRoute() {
  routeStops.value = []
  routeInfo.value = null
  routeLayer.clearLayers()
}

function haversineKm(a, b) {
  const R = 6371
  const dLat = ((b.lat - a.lat) * Math.PI) / 180
  const dLng = ((b.lng - a.lng) * Math.PI) / 180
  const s =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((a.lat * Math.PI) / 180) *
      Math.cos((b.lat * Math.PI) / 180) *
      Math.sin(dLng / 2) ** 2
  return 2 * R * Math.asin(Math.sqrt(s))
}

function drawStopMarkers() {
  routeStops.value.forEach((s, i) => {
    const icon = L.divIcon({
      className: '',
      html: `<div class="route-pin">${i + 1}</div>`,
      iconSize: [26, 26],
      iconAnchor: [13, 13],
    })
    routeLayer.addLayer(L.marker([s.lat, s.lng], { icon, zIndexOffset: 1000 }))
  })
}

async function drawRoute() {
  routeLayer.clearLayers()
  routeInfo.value = null
  if (routeStops.value.length === 0) return

  drawStopMarkers()
  if (routeStops.value.length < 2) return

  routing.value = true
  try {
    // OSRM 공개 데모 서버로 실제 도로 경로 조회 (API 키 불필요)
    const coords = routeStops.value.map((s) => `${s.lng},${s.lat}`).join(';')
    const res = await fetch(
      `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`
    )
    const data = await res.json()
    if (data.code !== 'Ok') throw new Error('route failed')

    const route = data.routes[0]
    const latlngs = route.geometry.coordinates.map(([lng, lat]) => [lat, lng])
    routeLayer.addLayer(
      L.polyline(latlngs, { color: '#e8a52a', weight: 5, opacity: 0.85 })
    )
    routeInfo.value = {
      distanceKm: (route.distance / 1000).toFixed(1),
      durationMin: Math.round(route.duration / 60),
      isStraight: false,
    }
    map.fitBounds(L.latLngBounds(latlngs), { padding: [40, 40] })
  } catch {
    // 라우팅 서버 실패 시 직선 연결로 폴백
    const latlngs = routeStops.value.map((s) => [s.lat, s.lng])
    routeLayer.addLayer(
      L.polyline(latlngs, {
        color: '#e8a52a',
        weight: 4,
        opacity: 0.8,
        dashArray: '8 8',
      })
    )
    let total = 0
    for (let i = 1; i < routeStops.value.length; i++) {
      total += haversineKm(routeStops.value[i - 1], routeStops.value[i])
    }
    routeInfo.value = {
      distanceKm: total.toFixed(1),
      durationMin: null,
      isStraight: true,
    }
    map.fitBounds(L.latLngBounds(latlngs), { padding: [40, 40] })
  } finally {
    routing.value = false
  }
}

onMounted(async () => {
  map = L.map(mapEl.value, { scrollWheelZoom: true }).setView(
    [36.4, 127.35],
    9
  )
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)

  markerLayer = L.layerGroup().addTo(map)
  routeLayer = L.layerGroup().addTo(map)

  await fetchAll()
  renderMarkers()
})

onBeforeUnmount(() => {
  if (map) map.remove()
})
</script>

<template>
  <PageLayout>

    <div class="map-head">
      <span class="map-head__emoji">🗺️</span>
      <h1>여행 지도</h1>
      <p>관광지와 맛집을 지도에서 한눈에 보고, 나만의 코스를 만들어보세요</p>
    </div>

    <!-- 필터 -->
    <div class="filter-row">
      <div class="chips">
        <button
          v-for="t in types"
          :key="t"
          :class="{ active: t === activeType }"
          @click="selectType(t)"
        >
          <span
            v-if="t !== '전체'"
            class="dot"
            :style="{ background: TYPE_META[t].color }"
          ></span>
          {{ t }}
        </button>
      </div>
      <div class="chips">
        <button
          v-for="r in regions"
          :key="r"
          :class="{ active: (r === '전체' && !activeRegion) || r === activeRegion }"
          @click="selectRegion(r)"
        >
          {{ r }}
        </button>
      </div>
    </div>

    <p class="count-line" v-if="!loading">
      지도에 <strong>{{ visibleCount.toLocaleString() }}</strong>곳 표시 중
      · 핀을 눌러 "경로에 추가"하면 이동 경로를 그려드려요
    </p>

    <div class="map-wrap">
      <div ref="mapEl" class="map-container"></div>
      <div v-if="loading" class="map-loading">장소를 불러오는 중...</div>
    </div>

    <!-- 경로 패널 -->
    <div v-if="routeStops.length" class="route-panel">
      <div class="route-panel__head">
        <h2>🚗 나의 여행 코스</h2>
        <button class="route-panel__clear" @click="clearRoute">전체 삭제</button>
      </div>

      <ol class="route-list">
        <li v-for="(s, i) in routeStops" :key="s.content_id">
          <span class="route-list__num">{{ i + 1 }}</span>
          <span class="route-list__title">{{ s.title }}</span>
          <span class="route-list__type">{{ s.type }}</span>
          <button class="route-list__remove" @click="removeStop(i)">×</button>
        </li>
      </ol>

      <p v-if="routing" class="route-summary">경로 계산 중...</p>
      <p v-else-if="routeInfo" class="route-summary">
        총 이동 거리 <strong>{{ routeInfo.distanceKm }}km</strong>
        <template v-if="routeInfo.durationMin !== null">
          · 예상 <strong>약 {{ routeInfo.durationMin }}분</strong> (자동차 기준)
        </template>
        <template v-if="routeInfo.isStraight">
          <br /><span class="route-summary__note"
            >※ 경로 서버 연결 실패로 직선 거리로 표시했어요</span
          >
        </template>
      </p>
      <p v-else-if="routeStops.length === 1" class="route-summary">
        장소를 하나 더 추가하면 경로가 그려져요
      </p>
    </div>

  </PageLayout>
</template>

<style scoped>
.map-head {
  text-align: center;
  margin-bottom: 24px;
}

.map-head__emoji {
  font-size: 30px;
}

.map-head h1 {
  margin-top: 4px;
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.05em;
  color: var(--color-brown-900);
}

.map-head p {
  margin-top: 8px;
  font-size: 15px;
  color: var(--color-brown-500);
}

.filter-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}

.chips button {
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

.chips button:hover {
  background: var(--color-cream-300);
}

.chips button.active {
  background: var(--color-gold-400);
  border-color: var(--color-gold-500);
  color: var(--color-brown-900);
}

.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.count-line {
  margin-bottom: 12px;
  text-align: center;
  font-size: 13px;
  color: var(--color-brown-500);
}

.count-line strong {
  color: var(--color-brown-800);
}

.map-wrap {
  position: relative;
  overflow: hidden;
  border: 1px solid #eed9b4;
  border-radius: 22px;
  box-shadow: var(--shadow-small);
}

.map-container {
  height: 560px;
  z-index: 1;
}

.map-loading {
  position: absolute;
  inset: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 249, 237, 0.85);
  color: var(--color-brown-700);
  font-weight: 700;
}

/* 팝업 (Leaflet이 body에 붙이므로 :deep 불필요, 전역 클래스로) */
:global(.map-popup__type) {
  font-size: 11px;
  font-weight: 700;
  color: #927056;
}

:global(.map-popup__title) {
  margin-top: 2px;
  font-size: 15px;
  font-weight: 800;
  color: #3f2819;
}

:global(.map-popup__addr) {
  margin-top: 4px;
  font-size: 12px;
  color: #927056;
  line-height: 1.5;
}

:global(.map-popup__btns) {
  display: flex;
  gap: 6px;
  margin-top: 10px;
}

:global(.map-popup__btn) {
  padding: 6px 12px;
  background: #fff1d6;
  border: 1px solid #e5c085;
  border-radius: 999px;
  color: #4b2f1d;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

:global(.map-popup__btn--gold) {
  background: #f3b940;
  border-color: #e8a52a;
}

:global(.route-pin) {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  background: #3f2819;
  border: 2px solid #fffdf8;
  border-radius: 50%;
  color: #ffd064;
  font-size: 13px;
  font-weight: 800;
  box-shadow: 0 3px 8px rgba(63, 40, 25, 0.35);
}

/* 경로 패널 */
.route-panel {
  margin-top: 18px;
  padding: 22px 26px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 20px;
  box-shadow: var(--shadow-small);
}

.route-panel__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.route-panel__head h2 {
  font-size: 18px;
  font-weight: 800;
  color: var(--color-brown-900);
}

.route-panel__clear {
  padding: 6px 14px;
  background: #fdeeee;
  border: 1.5px solid #f0c4bf;
  border-radius: 999px;
  color: #c0392b;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.route-list {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  list-style: none;
  padding: 0;
}

.route-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: #fffaf0;
  border: 1px solid #f0deba;
  border-radius: 14px;
}

.route-list__num {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  background: var(--color-brown-900);
  border-radius: 50%;
  color: var(--color-gold-300);
  font-size: 12px;
  font-weight: 800;
}

.route-list__title {
  flex: 1;
  min-width: 0;
  font-size: 14px;
  font-weight: 700;
  color: var(--color-brown-900);
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.route-list__type {
  font-size: 12px;
  color: var(--color-brown-500);
}

.route-list__remove {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  background: transparent;
  border: 0;
  color: var(--color-brown-500);
  font-size: 18px;
  cursor: pointer;
}

.route-summary {
  margin-top: 14px;
  font-size: 14px;
  color: var(--color-brown-700);
}

.route-summary strong {
  color: var(--color-brown-900);
}

.route-summary__note {
  font-size: 12px;
  color: var(--color-brown-500);
}

@media (max-width: 640px) {
  .map-head h1 {
    font-size: 28px;
  }

  .map-container {
    height: 420px;
  }
}
</style>