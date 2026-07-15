<script setup>
import { ref, onMounted } from "vue";
import api from "../../api";

const items = ref([]);
const loading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    const response = await api.get("/api/weather");
    items.value = response.data.items ?? [];
  } catch (error) {
    items.value = [];
    errorMessage.value = "날씨 정보를 불러오지 못했습니다.";
    console.error("날씨 정보 조회 실패:", error);
  } finally {
    loading.value = false;
  }
});

function gradeClass(grade) {
  return {
    좋음: "good",
    보통: "soso",
    나쁨: "bad",
  }[grade] || "";
}

function weatherIcon(description) {
  if (!description) {
    return "🌤️";
  }

  if (description.includes("맑음")) {
    return "☀️";
  }

  if (description.includes("구름")) {
    return "🌤️";
  }

  if (description.includes("비")) {
    return "🌧️";
  }

  if (description.includes("눈")) {
    return "🌨️";
  }

  if (description.includes("안개")) {
    return "🌫️";
  }

  return "🌤️";
}
</script>

<template>
  <section class="weather-widget">
    <div class="weather-header">
      <div>
        <h2 class="weather-title">오늘의 권역 날씨</h2>
        <p class="weather-subtitle">대전·충청 지역 여행 적합도</p>
      </div>
    </div>

    <div v-if="loading" class="weather-state">
      날씨 정보를 불러오는 중입니다.
    </div>

    <div v-else-if="errorMessage" class="weather-state weather-state--error">
      {{ errorMessage }}
    </div>

    <div v-else-if="items.length === 0" class="weather-state">
      표시할 날씨 정보가 없습니다.
    </div>

    <div v-else class="region-grid">
      <article
        v-for="weather in items"
        :key="weather.region"
        class="region-card"
      >
        <template v-if="!weather.error">
          <div class="region-card__top">
            <span class="region-name">
              {{ weather.region }}
            </span>

            <span class="weather-icon">
              {{ weatherIcon(weather.desc) }}
            </span>
          </div>

          <div class="weather-main">
            <strong class="temperature">
              {{ Math.round(weather.temp) }}°
            </strong>

            <span class="weather-description">
              {{ weather.desc }}
            </span>
          </div>

          <div
            class="travel-grade"
            :class="gradeClass(weather.travel.grade)"
          >
            {{ weather.travel.emoji }}
            {{ weather.travel.grade }}
          </div>

          <p class="travel-comment">
            {{ weather.travel.comment }}
          </p>
        </template>

        <template v-else>
          <div class="region-card__top">
            <span class="region-name">
              {{ weather.region }}
            </span>

            <span class="weather-icon">
              ⚠️
            </span>
          </div>

          <p class="region-error">
            날씨 정보를 조회하지 못했습니다.
          </p>
        </template>
      </article>
    </div>
  </section>
</template>

<style scoped>
.weather-widget {
  width: min(1100px, calc(100% - 40px));
  margin: 24px auto;
  padding: 24px 30px 30px;
  box-sizing: border-box;
  background: #fffaf0;
  border: 1px solid #e8c98c;
  border-radius: 20px;
}

.weather-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.weather-title {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #5b3518;
}

.weather-subtitle {
  margin: 6px 0 0;
  font-size: 13px;
  color: #8a6234;
}

.weather-state {
  padding: 36px 0;
  text-align: center;
  font-size: 14px;
  color: #806040;
}

.weather-state--error {
  color: #c65353;
}

.region-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.region-card {
  min-width: 0;
  padding: 18px;
  box-sizing: border-box;
  background: #ffffff;
  border: 1px solid #edd9b5;
  border-radius: 16px;
}

.region-card__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.region-name {
  font-size: 14px;
  font-weight: 700;
  color: #8a6234;
}

.weather-icon {
  font-size: 24px;
}

.weather-main {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  margin-top: 12px;
}

.temperature {
  font-size: 34px;
  line-height: 1;
  color: #5b3518;
}

.weather-description {
  padding-bottom: 3px;
  font-size: 14px;
  color: #806040;
}

.travel-grade {
  width: fit-content;
  margin-top: 14px;
  padding: 5px 10px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 999px;
}

.travel-grade.good {
  color: #1b8f5a;
  background: #e6f6ee;
}

.travel-grade.soso {
  color: #b7791f;
  background: #fdf3e1;
}

.travel-grade.bad {
  color: #c65353;
  background: #fdeaea;
}

.travel-comment {
  margin: 9px 0 0;
  font-size: 12px;
  line-height: 1.5;
  color: #806040;
}

.region-error {
  margin: 18px 0 0;
  font-size: 13px;
  line-height: 1.5;
  color: #c65353;
}

@media (max-width: 900px) {
  .region-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 600px) {
  .weather-widget {
    width: calc(100% - 24px);
    padding: 20px;
  }

  .region-grid {
    grid-template-columns: 1fr;
  }
}
</style>