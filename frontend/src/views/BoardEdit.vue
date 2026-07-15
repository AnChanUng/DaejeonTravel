<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import BaseButton from '../components/BaseButton.vue'
import PageLayout from '../components/layout/PageLayout.vue'

const route = useRoute()
const router = useRouter()
const form = reactive({ title: '', content: '', tags: '' })
const loaded = ref(false)
const submitting = ref(false)
const uploading = ref(false)
const password = sessionStorage.getItem('editPw') || ''

const imageFile = ref(null)
const imagePreview = ref('')   // 새로 고른 이미지 미리보기
const existingImage = ref('')  // 기존에 저장돼 있던 이미지
const removeExistingImage = ref(false)

function tagsToInput(tags) {
  return Array.isArray(tags) ? tags.join(', ') : ''
}

function normalizeTags(raw) {
  return raw
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean)
    .join(',')
}

onMounted(async () => {
  if (!password) {
    alert('비밀번호 확인이 필요합니다')
    return router.replace(`/community/${route.params.id}`)
  }
  try {
    // for_edit=true → 수정 화면 진입은 조회수에 반영하지 않음
    const res = await api.get(`/api/posts/${route.params.id}`, {
      params: { for_edit: true },
    })
    form.title = res.data.title
    form.content = res.data.content
    form.tags = tagsToInput(res.data.tags)
    existingImage.value = res.data.image || ''
    loaded.value = true
  } catch {
    alert('게시글을 불러오지 못했습니다')
    router.replace('/community')
  }
})

function onImageSelect(e) {
  const file = e.target.files?.[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) {
    alert('이미지 용량은 5MB를 넘을 수 없어요')
    e.target.value = ''
    return
  }
  imageFile.value = file
  imagePreview.value = URL.createObjectURL(file)
  removeExistingImage.value = false
}

function removeImage() {
  imageFile.value = null
  imagePreview.value = ''
  removeExistingImage.value = true
}

async function uploadImageIfNeeded() {
  if (!imageFile.value) return undefined // 이미지 변경 없음
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

async function submit() {
  if (!form.title.trim()) return alert('제목을 입력해주세요')
  if (!form.content.trim()) return alert('내용을 입력해주세요')

  submitting.value = true
  try {
    const uploadedUrl = await uploadImageIfNeeded()
    const finalImage = removeExistingImage.value
      ? null
      : uploadedUrl !== undefined
        ? uploadedUrl
        : existingImage.value || null

    await api.put(`/api/posts/${route.params.id}`, {
      title: form.title,
      content: form.content,
      password,
      image: finalImage,
      tags: normalizeTags(form.tags) || null,
    })
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

        <div v-if="imagePreview || (existingImage && !removeExistingImage)" class="image-preview">
          <img :src="imagePreview || existingImage" alt="첨부 이미지" />
          <button type="button" class="image-preview__remove" @click="removeImage">
            × 삭제
          </button>
        </div>

        <div class="btn-row">
          <BaseButton variant="ghost" @click="router.back()">취소</BaseButton>
          <BaseButton :disabled="submitting || uploading" @click="submit">
            {{ uploading ? '이미지 업로드 중...' : submitting ? '수정 중...' : '수정 완료' }}
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