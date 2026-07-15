<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'
import { getBookmarkedIds } from '../utils/postReactions'

const router = useRouter()
const posts = ref([])
const loading = ref(true)

function goDetail(id) {
  router.push(`/community/${id}`)
}

function formatDate(dt) {
  return dt ? dt.slice(0, 10).replaceAll('-', '.') : ''
}

onMounted(async () => {
  const ids = getBookmarkedIds()
  if (ids.length === 0) {
    loading.value = false
    return
  }
  try {
    const res = await api.post('/api/posts/batch', ids)
    // 북마크한 순서(최근 추가 순)와 비슷하게 id 내림차순 정렬
    posts.value = res.data.items.sort((a, b) => b.id - a.id)
  } catch {
    posts.value = []
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <PageLayout>

    <button class="back" @click="router.push('/community')">‹ 목록으로</button>

    <div class="board-head">
      <span class="board-head__bread">🔖</span>
      <h1>북마크한 게시글</h1>
      <p>이 기기에서 북마크한 글만 모아 볼 수 있어요</p>
    </div>

    <div v-if="loading" class="state-box">불러오는 중...</div>

    <div v-else-if="posts.length" class="card-list">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-card"
        @click="goDetail(post.id)"
      >
        <img
          v-if="post.image"
          :src="post.image"
          class="post-card__thumb"
          alt=""
        />
        <div v-else class="post-card__thumb post-card__thumb--empty">📝</div>

        <div class="post-card__info">
          <span class="badge">{{ post.category }}</span>
          <p class="post-card__title">{{ post.title }}</p>
          <div class="post-card__meta">
            <span>{{ formatDate(post.created_at) }}</span>
            <span>👁 {{ post.view_count }}</span>
            <span>❤️ {{ post.like_count }}</span>
          </div>
        </div>

        <span class="arrow">›</span>
      </div>
    </div>

    <div v-else class="state-box">
      <p>아직 북마크한 게시글이 없어요</p>
      <BaseButton @click="router.push('/community')">게시판 둘러보기</BaseButton>
    </div>

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

.board-head {
  text-align: center;
  margin-bottom: 28px;
}

.board-head__bread {
  font-size: 28px;
}

.board-head h1 {
  margin-top: 4px;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--color-brown-900);
}

.board-head p {
  margin-top: 8px;
  font-size: 14px;
  color: var(--color-brown-500);
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.post-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
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

.post-card__thumb {
  flex-shrink: 0;
  width: 76px;
  height: 76px;
  border-radius: 14px;
  object-fit: cover;
  background: var(--color-cream-300);
}

.post-card__thumb--empty {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  opacity: 0.5;
}

.post-card__info {
  flex: 1;
  min-width: 0;
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
  margin-top: 7px;
  font-size: 16px;
  font-weight: 700;
  color: var(--color-brown-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-card__meta {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  font-size: 12px;
  color: var(--color-brown-500);
}

.arrow {
  flex-shrink: 0;
  font-size: 22px;
  color: #cba76f;
}

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
</style>