<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'

const route = useRoute()
const router = useRouter()
const form = reactive({ title: '', content: '' })
const loaded = ref(false)
const submitting = ref(false)
const password = sessionStorage.getItem('editPw') || ''

onMounted(async () => {
  if (!password) {
    alert('비밀번호 확인이 필요합니다')
    return router.replace(`/community/${route.params.id}`)
  }
  try {
    const res = await api.get(`/api/posts/${route.params.id}`)
    form.title = res.data.title
    form.content = res.data.content
    loaded.value = true
  } catch {
    alert('게시글을 불러오지 못했습니다')
    router.replace('/community')
  }
})

async function submit() {
  if (!form.title.trim()) return alert('제목을 입력해주세요')
  if (!form.content.trim()) return alert('내용을 입력해주세요')

  submitting.value = true
  try {
    await api.put(`/api/posts/${route.params.id}`, { ...form, password })
    sessionStorage.removeItem('editPw')
    alert('수정되었습니다')
    router.push(`/community/${route.params.id}`)
  } catch (e) {
    if (e.response?.status === 403) {
      alert('비밀번호가 일치하지 않습니다')
      sessionStorage.removeItem('editPw')
      router.replace(`/community/${route.params.id}`)
    } else {
      alert('오류가 발생했습니다')
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <PageLayout>

    <template v-if="loaded">
      <div class="board-head">
        <span class="board-head__bread">📝</span>
        <h1>게시글 수정</h1>
      </div>

      <div class="form-card">
        <label>제목</label>
        <input v-model="form.title" />

        <label>내용</label>
        <textarea v-model="form.content" rows="10"></textarea>

        <div class="btn-row">
          <BaseButton variant="ghost" @click="router.back()">취소</BaseButton>
          <BaseButton :disabled="submitting" @click="submit">
            {{ submitting ? '수정 중...' : '수정 완료' }}
          </BaseButton>
        </div>
      </div>
    </template>

  </PageLayout>
</template>

<style scoped>
.board-head {
  text-align: center;
  margin-bottom: 28px;
}

.board-head__bread {
  font-size: 26px;
}

.board-head h1 {
  margin-top: 4px;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--color-brown-900);
}

.form-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 32px;
  background: var(--color-cream-100);
  border: 1px solid #eed9b4;
  border-radius: 20px;
  box-shadow: var(--shadow-small);
}

label {
  margin-top: 10px;
  font-size: 13px;
  font-weight: 700;
  color: var(--color-brown-700);
}

input,
textarea {
  padding: 13px 16px;
  background: #fff;
  border: 1.5px solid #dbb87e;
  border-radius: 14px;
  font-size: 15px;
  color: var(--color-brown-900);
  outline: none;
  resize: vertical;
}

input:focus,
textarea:focus {
  border-color: var(--color-gold-500);
}

.btn-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}
</style>