<template>
  <div class="weather-card">
    <h2>오늘의 권역 날씨</h2>
    <p class="sub">대전·충청 지역 여행 적합도</p>

    <div v-if="loading" class="loading">불러오는 중...</div>

    <div v-else class="region-grid">
      <div v-for="w in items" :key="w.region" class="region-item">
        <template v-if="!w.error">
          <span class="region-name">{{ w.region }}</span>
          <span class="temp">{{ Math.round(w.temp) }}°</span>
          <span class="desc">{{ w.desc }}</span>
          <div class="travel" :class="gradeClass(w.travel.grade)">
            {{ w.travel.emoji }} {{ w.travel.grade }}
          </div>
          <p class="comment">{{ w.travel.comment }}</p>
        </template>
        <template v-else>
          <span class="region-name">{{ w.region }}</span>
          <span class="desc">조회 실패</span>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const items = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await api.get("/api/weather");
    items.value = res.data.items;
  } catch {
    items.value = [];
  } finally {
    loading.value = false;
  }
});

function gradeClass(grade) {
  return { 좋음: "good", 보통: "soso", 나쁨: "bad" }[grade] || "";
}
</script>

<style scoped>
.weather-card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-card);
}
h2 {
  font-size: 18px;
  font-weight: 800;
}
.sub {
  font-size: 13px;
  color: var(--color-text-sub);
  margin-bottom: 16px;
}
.loading {
  color: var(--color-text-sub);
  padding: 20px 0;
  text-align: center;
}

.region-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}
.region-item {
  background: var(--color-bg);
  border-radius: var(--radius-md);
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.region-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-sub);
}
.temp {
  font-size: 26px;
  font-weight: 800;
}
.desc {
  font-size: 13px;
}
.travel {
  margin-top: 6px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 8px;
  padding: 3px 8px;
  width: fit-content;
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
  color: var(--color-danger);
  background: var(--color-danger-bg);
}
.comment {
  font-size: 12px;
  color: var(--color-text-sub);
  margin-top: 4px;
}
</style>
