<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'

const router = useRouter()
const submitting = ref(false)

const form = reactive({
  category: '관광지',
  title: '',
  content: '',
  password: '',
})

async function submit() {
  if (!form.title.trim()) return alert('제목을 입력해주세요')
  if (!form.content.trim()) return alert('내용을 입력해주세요')
  if (!form.password.trim()) return alert('비밀번호를 입력해주세요')

  submitting.value = true
  try {
    const res = await api.post('/api/posts', form)
    router.push(`/community/${res.data.id}`)
  } catch {
    alert('등록 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <PageLayout>

    <div class="board-head">
      <span class="board-head__bread">✏️</span>
      <h1>게시글 작성</h1>
      <p>대전·충청 이야기를 들려주세요</p>
    </div>

    <div class="form-card">
      <label>카테고리</label>
      <select v-model="form.category">
        <option>관광지</option>
        <option>맛집</option>
        <option>축제·행사</option>
        <option>자유</option>
      </select>

      <label>제목</label>
      <input v-model="form.title" placeholder="제목을 입력하세요" />

      <label>내용</label>
      <textarea
        v-model="form.content"
        rows="10"
        placeholder="내용을 입력하세요"
      ></textarea>

      <label>수정용 비밀번호</label>
      <input
        v-model="form.password"
        type="password"
        placeholder="수정·삭제 시 사용됩니다"
      />
      <p class="hint">※ 게시글 수정·삭제 확인용으로 사용됩니다</p>

      <div class="btn-row">
        <BaseButton variant="ghost" @click="router.back()">취소</BaseButton>
        <BaseButton :disabled="submitting" @click="submit">
          {{ submitting ? '등록 중...' : '등록' }}
        </BaseButton>
      </div>
    </div>

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

.board-head p {
  margin-top: 8px;
  font-size: 14px;
  color: var(--color-brown-500);
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
textarea,
select {
  padding: 13px 16px;
  background: #fff;
  border: 1.5px solid #dbb87e;
  border-radius: 14px;
  font-size: 15px;
  color: var(--color-brown-900);
  outline: none;
  resize: vertical;
}

input::placeholder,
textarea::placeholder {
  color: #b99b74;
}

input:focus,
textarea:focus,
select:focus {
  border-color: var(--color-gold-500);
}

.hint {
  font-size: 12px;
  color: var(--color-brown-500);
}

.btn-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}
</style>