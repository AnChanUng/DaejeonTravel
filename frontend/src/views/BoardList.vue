<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'

const router = useRouter()
const posts = ref([])
const keyword = ref('')
const category = ref('')
const page = ref(1)
const size = 10
const total = ref(0)
const loading = ref(true)

const categories = ['전체', '관광지', '맛집', '축제·행사', '자유']

const totalPages = computed(() => Math.ceil(total.value / size))

async function fetchPosts() {
  loading.value = true
  try {
    const res = await api.get('/api/posts', {
      params: {
        keyword: keyword.value || undefined,
        category: category.value || undefined,
        page: page.value,
        size,
      },
    })
    posts.value = res.data.items
    total.value = res.data.total
  } catch {
    posts.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function search() {
  page.value = 1
  fetchPosts()
}

function selectCategory(c) {
  category.value = c === '전체' ? '' : c
  page.value = 1
  fetchPosts()
}

function movePage(p) {
  page.value = p
  fetchPosts()
}

function goDetail(id) {
  router.push(`/community/${id}`)
}

function goWrite() {
  router.push('/community/write')
}

function formatDate(dt) {
  return dt ? dt.slice(0, 10).replaceAll('-', '.') : ''
}

onMounted(fetchPosts)
</script>

<template>
  <PageLayout>

    <div class="board-head">
      <span class="board-head__bread">🥐</span>
      <h1>커뮤니티</h1>
      <p>대전·충청 지역 이야기를 나눠보세요</p>
    </div>

    <!-- 카테고리 탭 -->
    <div class="category-tabs">
      <button
        v-for="c in categories"
        :key="c"
        :class="{ active: (c === '전체' && !category) || c === category }"
        @click="selectCategory(c)"
      >
        {{ c }}
      </button>
    </div>

    <!-- 검색 + 글쓰기 -->
    <div class="top-bar">
      <div class="search-box">
        <span class="search-box__icon">🔍</span>
        <input
          v-model="keyword"
          @keyup.enter="search"
          placeholder="제목으로 검색해보세요"
        />
      </div>
      <BaseButton @click="goWrite">✏️ 글쓰기</BaseButton>
    </div>

    <!-- 게시글 목록 -->
    <div v-if="loading" class="state-box">불러오는 중...</div>

    <div v-else class="card-list">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-card"
        @click="goDetail(post.id)"
      >
        <div class="post-card__info">
          <span class="badge">{{ post.category }}</span>
          <p class="post-card__title">{{ post.title }}</p>
          <span class="post-card__date">{{ formatDate(post.created_at) }}</span>
        </div>
        <span class="post-card__arrow">›</span>
      </div>

      <div v-if="posts.length === 0" class="state-box">
        <p>아직 게시글이 없어요</p>
        <BaseButton @click="goWrite">첫 글 작성하기</BaseButton>
      </div>
    </div>

    <!-- 페이지네이션 -->
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
      <button :disabled="page === totalPages" @click="movePage(page + 1)">›</button>
    </div>

  </PageLayout>
</template>

<style scoped>

/* 페이지 헤드 — 메인 히어로와 같은 톤 */
.board-head {
  text-align: center;
  margin-bottom: 28px;
}

.board-head__bread {
  font-size: 28px;
}

.board-head h1 {
  margin-top: 4px;
  font-size: 34px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--color-brown-900);
}

.board-head p {
  margin-top: 8px;
  font-size: 15px;
  color: var(--color-brown-500);
}

/* 카테고리 탭 */
.category-tabs {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 22px;
}

.category-tabs button {
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

.category-tabs button:hover {
  background: var(--color-cream-300);
}

.category-tabs button.active {
  background: var(--color-gold-400);
  border-color: var(--color-gold-500);
  color: var(--color-brown-900);
}

/* 검색 — 메인 검색창과 같은 알약형 */
.top-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 18px;
  background: #fff;
  border: 1.5px solid #dbb87e;
  border-radius: 999px;
  box-shadow: 0 6px 18px rgba(91, 57, 21, 0.08);
}

.search-box__icon {
  font-size: 16px;
}

.search-box input {
  flex: 1;
  padding: 13px 0;
  border: 0;
  outline: 0;
  background: transparent;
  font-size: 15px;
  color: var(--color-brown-900);
}

.search-box input::placeholder {
  color: #b99b74;
}

/* 게시글 카드 */
.card-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.post-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 18px;
  box-shadow: var(--shadow-small);
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  background: var(--color-cream-300);
  border: 1px solid #e5c085;
  border-radius: 999px;
  color: var(--color-brown-700);
  font-size: 12px;
  font-weight: 700;
}

.post-card__title {
  margin-top: 8px;
  font-size: 16px;
  font-weight: 700;
  color: var(--color-brown-900);
}

.post-card__date {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: var(--color-brown-500);
}

.post-card__arrow {
  font-size: 22px;
  color: #cba76f;
}

/* 빈 상태 / 로딩 */
.state-box {
  padding: 60px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background: var(--color-cream-100);
  border: 1px dashed #dbb87e;
  border-radius: 18px;
  color: var(--color-brown-500);
  font-size: 15px;
  text-align: center;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 28px;
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

@media (max-width: 520px) {
  .board-head h1 {
    font-size: 26px;
  }

  .top-bar {
    flex-direction: column;
  }
}
</style>