<template>
  <div>
    <WeatherWidget style="margin-bottom: 20px" />
    <div class="page-head">
      <h1>커뮤니티</h1>
      <p class="sub">대전·충청 지역 이야기를 나눠보세요</p>
    </div>

    <div class="top-bar">
      <input
        v-model="keyword"
        @keyup.enter="fetchPosts"
        placeholder="제목으로 검색"
      />
      <BaseButton @click="goWrite">글쓰기</BaseButton>
    </div>

    <div class="card-list">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-card"
        @click="goDetail(post.id)"
      >
        <div class="post-info">
          <span class="badge">{{ post.category }}</span>
          <p class="post-title">{{ post.title }}</p>
          <span class="post-date">{{ formatDate(post.created_at) }}</span>
        </div>
        <span class="arrow">›</span>
      </div>

      <div v-if="posts.length === 0" class="empty">
        <p>아직 게시글이 없어요</p>
        <BaseButton @click="goWrite">첫 글 작성하기</BaseButton>
      </div>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page === 1" @click="movePage(page - 1)">‹</button>
      <button
        v-for="p in totalPages"
        :key="p"
        :class="{ active: p === page }"
        @click="movePage(p)"
      >
        {{ p }}
      </button>
      <button :disabled="page === totalPages" @click="movePage(page + 1)">
        ›
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api";
import BaseButton from "../components/BaseButton.vue";
import WeatherWidget from "../components/weather/WeatherWidget.vue";

const router = useRouter();
const posts = ref([]);
const keyword = ref("");
const page = ref(1);
const size = 10;
const total = ref(0);

const totalPages = computed(() => Math.ceil(total.value / size));

async function fetchPosts() {
  const res = await api.get("/api/posts", {
    params: { keyword: keyword.value || undefined, page: page.value, size },
  });
  posts.value = res.data.items;
  total.value = res.data.total;
}

function movePage(p) {
  page.value = p;
  fetchPosts();
}

function goDetail(id) {
  router.push(`/board/${id}`);
}
function goWrite() {
  router.push("/board/write");
}
function formatDate(dt) {
  return dt ? dt.slice(0, 10).replaceAll("-", ".") : "";
}

onMounted(fetchPosts);
</script>

<style scoped>
.page-head {
  margin-bottom: 20px;
}
h1 {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.5px;
}
.sub {
  color: var(--color-text-sub);
  font-size: 14px;
  margin-top: 4px;
}

.top-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}
.top-bar input {
  flex: 1;
  padding: 14px 16px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-card);
  font-size: 15px;
  outline: none;
  box-shadow: var(--shadow-card);
}
.top-bar input:focus {
  box-shadow: 0 0 0 2px var(--color-primary);
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.post-card {
  background: var(--color-card);
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition:
    transform 0.12s,
    box-shadow 0.12s;
  box-shadow: var(--shadow-card);
}
.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

.badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary);
  background: #e8f1fe;
  border-radius: 8px;
  padding: 3px 8px;
  margin-bottom: 6px;
}
.post-title {
  font-size: 16px;
  font-weight: 600;
}
.post-date {
  font-size: 13px;
  color: var(--color-text-sub);
}
.arrow {
  color: #b0b8c1;
  font-size: 22px;
}

.empty {
  background: var(--color-card);
  border-radius: 16px;
  padding: 48px 20px;
  text-align: center;
  color: var(--color-text-sub);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 24px;
}
.pagination button {
  min-width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--color-card);
  color: #4e5968;
  font-weight: 600;
}
.pagination button.active {
  background: var(--color-primary);
  color: #fff;
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>
