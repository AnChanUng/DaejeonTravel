<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'

const router = useRouter()
const submitting = ref(false)
const uploading = ref(false)

const form = reactive({
  category: '관광지',
  title: '',
  content: '',
  password: '',
  tags: '', // "여행, 맛집, 대전" 형식으로 입력받음
})

const imageFile = ref(null)
const imagePreview = ref('')
const imageUrl = ref('') // 업로드 완료 후 서버에 저장된 경로

function onImageSelect(e) {
  const file = e.target.files?.[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    alert('이미지 용량은 5MB를 넘을 수 없어요')
    e.target.value = ''
    return
  }

  imageFile.value = file
  imageUrl.value = ''
  imagePreview.value = URL.createObjectURL(file)
}

function removeImage() {
  imageFile.value = null
  imageUrl.value = ''
  imagePreview.value = ''
}

async function uploadImageIfNeeded() {
  if (!imageFile.value) return ''
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', imageFile.value)
    const res = await api.post('/api/posts/upload', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return res.data.url
  } finally {
    uploading.value = false
  }
}

// "여행, 맛집,대전" → "여행,맛집,대전" (공백 정리, 빈 값 제거)
function normalizeTags(raw) {
  return raw
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean)
    .join(',')
}

async function submit() {
  if (!form.title.trim()) return alert('제목을 입력해주세요')
  if (!form.content.trim()) return alert('내용을 입력해주세요')
  if (!form.password.trim()) return alert('비밀번호를 입력해주세요')

  submitting.value = true
  try {
    const uploadedUrl = await uploadImageIfNeeded()

    const res = await api.post('/api/posts', {
      category: form.category,
      title: form.title,
      content: form.content,
      password: form.password,
      image: uploadedUrl || null,
      tags: normalizeTags(form.tags) || null,
    })
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

      <label>태그</label>
      <input
        v-model="form.tags"
        placeholder="쉼표로 구분해 입력하세요 (예: 맛집, 대전, 주말나들이)"
      />

      <label>사진 첨부</label>
      <div class="image-upload">
        <label class="image-upload__btn">
          📷 사진 선택
          <input
            type="file"
            accept="image/jpeg,image/png,image/gif,image/webp"
            @change="onImageSelect"
            hidden
          />
        </label>
        <span class="image-upload__hint">jpg·png·gif·webp / 최대 5MB</span>
      </div>

      <div v-if="imagePreview" class="image-preview">
        <img :src="imagePreview" alt="첨부 이미지 미리보기" />
        <button type="button" class="image-preview__remove" @click="removeImage">
          × 삭제
        </button>
      </div>

      <label>수정용 비밀번호</label>
      <input
        v-model="form.password"
        type="password"
        placeholder="수정·삭제 시 사용됩니다"
      />
      <p class="hint">※ 게시글 수정·삭제 확인용으로 사용됩니다</p>

      <div class="btn-row">
        <BaseButton variant="ghost" @click="router.back()">취소</BaseButton>
        <BaseButton :disabled="submitting || uploading" @click="submit">
          {{ uploading ? '이미지 업로드 중...' : submitting ? '등록 중...' : '등록' }}
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

/* 이미지 업로드 */
.image-upload {
  display: flex;
  align-items: center;
  gap: 10px;
}

.image-upload__btn {
  padding: 10px 18px;
  background: var(--color-cream-300);
  border: 1.5px solid #e5c085;
  border-radius: 999px;
  color: var(--color-brown-800);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.image-upload__btn:hover {
  background: var(--color-gold-300);
}

.image-upload__hint {
  font-size: 12px;
  color: var(--color-brown-500);
}

.image-preview {
  position: relative;
  width: fit-content;
  margin-top: 4px;
}

.image-preview img {
  max-width: 260px;
  max-height: 180px;
  border-radius: 14px;
  border: 1px solid #eed9b4;
  object-fit: cover;
}

.image-preview__remove {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 4px 10px;
  background: rgba(63, 40, 25, 0.75);
  border: 0;
  border-radius: 999px;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.btn-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}
</style>