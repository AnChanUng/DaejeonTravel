<script setup>
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../../api'

const { locale } = useI18n()

const items = ref([])
const loading = ref(true)


const fetchWeather = async () => {
  try {
    loading.value = true

    const res = await api.get(
      `/api/weather?lang=${locale.value}`
    )

    items.value = res.data.items

  } catch (error) {
    console.error('날씨 조회 실패:', error)
    items.value = []

  } finally {
    loading.value = false
  }
}


onMounted(() => {
  fetchWeather()
})


watch(
  locale,
  () => {
    fetchWeather()
  }
)


function gradeClass(grade) {
  return {
    좋음: 'good',
    보통: 'soso',
    나쁨: 'bad',
    Good: 'good',
    Normal: 'soso',
    Bad: 'bad'
  }[grade] || ''
}

</script>

<template>
  <div class="weather-card">

    <h2>
      ☀️ {{ $t('weather.title') }}
    </h2>

    <p class="sub">
      {{ $t('weather.subtitle') }}
    </p>


    <div v-if="loading" class="loading">
      {{ $t('weather.loading') }}
    </div>


    <div v-else class="region-grid">

      <div
        v-for="w in items"
        :key="w.region"
        class="region-item"
      >

        <template v-if="!w.error">

          <span class="region-name">
            {{ w.region }}
          </span>

          <span class="temp">
            {{ Math.round(w.temp) }}°
          </span>

          <span class="desc">
            {{ w.desc }}
          </span>


          <div
            class="travel"
            :class="gradeClass(w.travel.grade)"
          >
            {{ w.travel.emoji }}
            {{ w.travel.grade }}
          </div>


          <p class="comment">
            {{ w.travel.comment }}
          </p>

        </template>


        <template v-else>

          <span class="region-name">
            {{ w.region }}
          </span>

          <span class="desc">
            {{ $t('weather.failed') }}
          </span>

        </template>

      </div>

    </div>

  </div>
</template>

<style scoped>
/* 메인 '오늘의 대전 여행 날씨' 카드와 동일 계열 */
.weather-card {
  width: min(1100px, calc(100% - 40px));
  margin: 24px auto 40px;
  padding: 24px 28px;
  box-sizing: border-box;

  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 20px;
  box-shadow: var(--shadow-small);
}


h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: var(--color-brown-900);
  color: var(--color-brown-900);
}


.sub {
  margin-top: 4px;
  margin-top: 4px;
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--color-brown-500);
  font-size: 13px;
  color: var(--color-brown-500);
}


.loading {
  padding: 20px 0;
  text-align: center;
  color: var(--color-brown-500);
  color: var(--color-brown-500);
}

.region-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}


.region-item {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 14px 16px;

  background: #fffaf0;
  border: 1px solid #f0deba;
  border-radius: 16px;
}


.region-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-brown-500);
  color: var(--color-brown-500);
}


.temp {
  font-size: 26px;
  font-weight: 800;
  color: var(--color-brown-900);
  color: var(--color-brown-900);
}


.desc {
  font-size: 13px;
  color: var(--color-brown-700);
  color: var(--color-brown-700);
}


.travel {
  width: fit-content;
  margin-top: 6px;
  padding: 3px 9px;

  border-radius: 999px;
  font-size: 13px;
  font-weight: 700;
}


.travel.good {
  color: #1b8f5a;
  background: #e6f6ee;
}


.travel.soso {
  color: #b7791f;
  background: #fdf3e1;
}


.travel.bad {
  color: #c0392b;
  background: #fdeeee;
  color: #c0392b;
  background: #fdeeee;
}


.comment {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--color-brown-500);
}

@media (max-width: 900px) {
  .region-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 600px) {
  .weather-card {
    width: calc(100% - 24px);
    padding: 20px;
  }

  .region-grid {
    grid-template-columns: 1fr;
  }
}
</style>