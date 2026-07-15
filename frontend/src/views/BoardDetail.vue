<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const notFound = ref(false)

const showModal = ref(false)
const mode = ref('')
const password = ref('')
const errorMsg = ref('')

async function fetchPost() {
  try {
    const res = await api.get(`/api/posts/${route.params.id}`)
    post.value = res.data
  } catch {
    notFound.value = true
  }
}

function openModal(m) {
  mode.value = m
  password.value = ''
  errorMsg.value = ''
  showModal.value = true
}

async function confirm() {
  if (!password.value) {
    errorMsg.value = '비밀번호를 입력해주세요'
    return
  }

  if (mode.value === 'delete') {
    try {
      await api.delete(`/api/posts/${route.params.id}`, {
        data: { password: password.value },
      })
      alert('삭제되었습니다')
      router.push('/community')
    } catch (e) {
      errorMsg.value =
        e.response?.status === 403
          ? '비밀번호가 일치하지 않습니다'
          : '오류가 발생했습니다'
    }
  } else {
    sessionStorage.setItem('editPw', password.value)
    router.push(`/community/${route.params.id}/edit`)
  }
}

function formatDate(dt) {
  return dt ? dt.slice(0, 10).replaceAll('-', '.') : ''
}

onMounted(fetchPost)
</script>

<template>
  <PageLayout>

    <button class="back" @click="router.push('/community')">‹ 목록으로</button>

    <div v-if="notFound" class="state-box">
      <p>게시글을 찾을 수 없어요</p>
      <BaseButton @click="router.push('/community')">목록으로 돌아가기</BaseButton>
    </div>

    <template v-else-if="post">
      <div class="detail-card">
        <span class="badge">{{ post.category }}</span>
        <h1>{{ post.title }}</h1>
        <p class="date">{{ formatDate(post.created_at) }}</p>
        <hr />
        <p class="content">{{ post.content }}</p>
      </div>

      <div class="btn-row">
        <BaseButton variant="ghost" @click="openModal('edit')">수정</BaseButton>
        <BaseButton variant="danger" @click="openModal('delete')">삭제</BaseButton>
      </div>
    </template>

    <!-- 비밀번호 확인 모달 -->
    <div v-if="showModal" class="modal-bg" @click.self="showModal = false">
      <div class="modal">
        <h2>비밀번호 확인</h2>
        <p class="modal-sub">
          {{ mode === 'delete' ? '삭제하려면' : '수정하려면' }} 작성 시 입력한
          비밀번호가 필요해요
        </p>
        <input
          v-model="password"
          type="password"
          placeholder="비밀번호 입력"
          @keyup.enter="confirm"
          autofocus
        />
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
        <BaseButton class="full" @click="confirm">확인</BaseButton>
      </div>
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

.detail-card {
  padding: 32px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 20px;
  box-shadow: var(--shadow-small);
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
  margin-bottom: 12px;
}

h1 {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--color-brown-900);
}

.date {
  margin-top: 8px;
  font-size: 13px;
  color: var(--color-brown-500);
}

hr {
  margin: 20px 0;
  border: none;
  border-top: 1px solid #f0deba;
}

.content {
  font-size: 15px;
  line-height: 1.8;
  color: var(--color-brown-800);
  white-space: pre-wrap;
}

.btn-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
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
}

/* 모달 */
.modal-bg {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(63, 40, 25, 0.45);
}

.modal {
  width: 340px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 20px;
  box-shadow: var(--shadow-medium);
}

.modal h2 {
  font-size: 18px;
  font-weight: 800;
  text-align: center;
  color: var(--color-brown-900);
}

.modal-sub {
  font-size: 13px;
  text-align: center;
  color: var(--color-brown-500);
}

.modal input {
  padding: 13px 16px;
  border: 1.5px solid #dbb87e;
  border-radius: 14px;
  background: #fff;
  font-size: 15px;
  outline: none;
  color: var(--color-brown-900);
}

.modal input:focus {
  border-color: var(--color-gold-500);
}

.error {
  color: #c0392b;
  font-size: 13px;
}

.full {
  width: 100%;
}
</style>