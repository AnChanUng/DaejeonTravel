<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import Chart from 'chart.js/auto'
import api from '../api'
import PageLayout from '../components/layout/PageLayout.vue'

const router = useRouter()
const loading = ref(true)
const stats = ref(null)

const categoryChartEl = ref(null)
const regionChartEl = ref(null)
const typeChartEl = ref(null)
const topPostsChartEl = ref(null)

let charts = []

// 크림/골드 테마 팔레트
const PALETTE = ['#e8a52a', '#d97f5f', '#7fa06b', '#a67fb5', '#b99b74', '#f3b940']
const BROWN = '#4b2f1d'
const BROWN_SUB = '#927056'

Chart.defaults.font.family =
  "'Pretendard', 'Noto Sans KR', -apple-system, sans-serif"
Chart.defaults.color = BROWN_SUB

function makeChart(el, config) {
  const c = new Chart(el.getContext('2d'), config)
  charts.push(c)
  return c
}

function buildCharts() {
  const s = stats.value

  // 1) 카테고리별 게시글 수 — 세로 막대
  makeChart(categoryChartEl.value, {
    type: 'bar',
    data: {
      labels: s.posts.by_category.map((c) => c.category),
      datasets: [
        {
          label: '게시글 수',
          data: s.posts.by_category.map((c) => c.count),
          backgroundColor: PALETTE,
          borderRadius: 10,
          maxBarThickness: 52,
        },
      ],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#f0deba' } },
        x: { grid: { display: false }, ticks: { color: BROWN } },
      },
    },
  })

  // 2) 지역별 장소 분포 — 도넛
  makeChart(regionChartEl.value, {
    type: 'doughnut',
    data: {
      labels: s.locations.by_region.map((r) => r.region),
      datasets: [
        {
          data: s.locations.by_region.map((r) => r.count),
          backgroundColor: PALETTE,
          borderColor: '#fffdf8',
          borderWidth: 3,
        },
      ],
    },
    options: {
      cutout: '58%',
      plugins: {
        legend: { position: 'bottom', labels: { color: BROWN, boxWidth: 12 } },
      },
    },
  })

  // 3) 유형별 장소 수 — 가로 막대
  makeChart(typeChartEl.value, {
    type: 'bar',
    data: {
      labels: s.locations.by_type.map((t) => t.type),
      datasets: [
        {
          label: '장소 수',
          data: s.locations.by_type.map((t) => t.count),
          backgroundColor: '#f3b940',
          borderRadius: 10,
          maxBarThickness: 26,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#f0deba' } },
        y: { grid: { display: false }, ticks: { color: BROWN } },
      },
    },
  })

  // 4) 인기 게시글 TOP 5 (조회수) — 가로 막대
  if (s.posts.top_viewed.length) {
    makeChart(topPostsChartEl.value, {
      type: 'bar',
      data: {
        labels: s.posts.top_viewed.map((p) =>
          p.title.length > 16 ? p.title.slice(0, 16) + '…' : p.title
        ),
        datasets: [
          {
            label: '조회수',
            data: s.posts.top_viewed.map((p) => p.view_count),
            backgroundColor: '#d97f5f',
            borderRadius: 10,
            maxBarThickness: 26,
          },
        ],
      },
      options: {
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        onClick: (_, elements) => {
          if (elements.length) {
            const post = s.posts.top_viewed[elements[0].index]
            router.push(`/community/${post.id}`)
          }
        },
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#f0deba' } },
          y: { grid: { display: false }, ticks: { color: BROWN } },
        },
      },
    })
  }
}

onMounted(async () => {
  try {
    const res = await api.get('/api/stats')
    stats.value = res.data
    loading.value = false
    // DOM 렌더 후 차트 생성
    await Promise.resolve()
    setTimeout(buildCharts, 0)
  } catch {
    loading.value = false
  }
})

onBeforeUnmount(() => {
  charts.forEach((c) => c.destroy())
  charts = []
})
</script>

<template>
  <PageLayout>

    <div class="dash-head">
      <span class="dash-head__emoji">📊</span>
      <h1>서비스 대시보드</h1>
      <p>커뮤니티와 여행 데이터 현황을 한눈에 확인하세요</p>
    </div>

    <div v-if="loading" class="state-box">통계를 불러오는 중...</div>

    <template v-else-if="stats">
      <!-- 요약 카드 -->
      <div class="stat-cards">
        <div class="stat-card">
          <span class="stat-card__label">📝 총 게시글</span>
          <strong>{{ stats.posts.total.toLocaleString() }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-card__label">👁 총 조회수</span>
          <strong>{{ stats.posts.total_views.toLocaleString() }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-card__label">❤️ 총 좋아요</span>
          <strong>{{ stats.posts.total_likes.toLocaleString() }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-card__label">📍 등록 장소</span>
          <strong>{{ stats.locations.total.toLocaleString() }}</strong>
        </div>
      </div>

      <!-- 차트 그리드 -->
      <div class="chart-grid">
        <div class="chart-card">
          <h2>카테고리별 게시글</h2>
          <div class="chart-body">
            <canvas ref="categoryChartEl"></canvas>
          </div>
        </div>

        <div class="chart-card">
          <h2>지역별 장소 분포</h2>
          <div class="chart-body">
            <canvas ref="regionChartEl"></canvas>
          </div>
        </div>

        <div class="chart-card">
          <h2>유형별 등록 장소</h2>
          <div class="chart-body">
            <canvas ref="typeChartEl"></canvas>
          </div>
        </div>

        <div class="chart-card">
          <h2>인기 게시글 TOP 5 <span class="chart-card__hint">막대를 누르면 글로 이동</span></h2>
          <div class="chart-body">
            <canvas v-if="stats.posts.top_viewed.length" ref="topPostsChartEl"></canvas>
            <p v-else class="chart-empty">아직 게시글이 없어요</p>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="state-box">통계를 불러오지 못했어요. 잠시 후 다시 시도해주세요.</div>

  </PageLayout>
</template>

<style scoped>
.dash-head {
  text-align: center;
  margin-bottom: 28px;
}

.dash-head__emoji {
  font-size: 30px;
}

.dash-head h1 {
  margin-top: 4px;
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.05em;
  color: var(--color-brown-900);
}

.dash-head p {
  margin-top: 8px;
  font-size: 15px;
  color: var(--color-brown-500);
}

/* 요약 카드 */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 18px 20px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 18px;
  box-shadow: var(--shadow-small);
}

.stat-card__label {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-brown-500);
}

.stat-card strong {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--color-brown-900);
}

/* 차트 그리드 */
.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.chart-card {
  padding: 22px 24px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 20px;
  box-shadow: var(--shadow-small);
}

.chart-card h2 {
  margin-bottom: 14px;
  font-size: 16px;
  font-weight: 800;
  color: var(--color-brown-900);
}

.chart-card__hint {
  margin-left: 6px;
  font-size: 11px;
  font-weight: 400;
  color: var(--color-brown-500);
}

.chart-body {
  position: relative;
  height: 260px;
}

.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--color-brown-500);
  font-size: 14px;
}

.state-box {
  padding: 70px 0;
  text-align: center;
  background: var(--color-cream-100);
  border: 1px dashed #dbb87e;
  border-radius: 18px;
  color: var(--color-brown-500);
  font-weight: 700;
}

@media (max-width: 768px) {
  .stat-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-grid {
    grid-template-columns: 1fr;
  }

  .dash-head h1 {
    font-size: 28px;
  }
}
</style>