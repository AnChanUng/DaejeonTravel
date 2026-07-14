<template>
  <div v-if="loaded">
    <h1>게시글 수정</h1>

    <div class="form-card">
      <label>제목</label>
      <input v-model="form.title" />

      <label>내용</label>
      <textarea v-model="form.content" rows="10"></textarea>

      <div class="btn-row">
        <BaseButton variant="ghost" @click="$router.back()">취소</BaseButton>
        <BaseButton @click="submit">수정 완료</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../api";
import BaseButton from "../components/BaseButton.vue";

const route = useRoute();
const router = useRouter();
const form = reactive({ title: "", content: "" });
const loaded = ref(false);
const password = sessionStorage.getItem("editPw") || "";

onMounted(async () => {
  if (!password) {
    alert("비밀번호 확인이 필요합니다");
    return router.replace(`/board/${route.params.id}`);
  }
  const res = await api.get(`/api/posts/${route.params.id}`);
  form.title = res.data.title;
  form.content = res.data.content;
  loaded.value = true;
});

async function submit() {
  if (!form.title.trim()) return alert("제목을 입력해주세요");
  try {
    await api.put(`/api/posts/${route.params.id}`, { ...form, password });
    sessionStorage.removeItem("editPw");
    alert("수정되었습니다");
    router.push(`/board/${route.params.id}`);
  } catch (e) {
    if (e.response?.status === 403) {
      alert("비밀번호가 일치하지 않습니다");
      sessionStorage.removeItem("editPw");
      router.replace(`/board/${route.params.id}`);
    } else {
      alert("오류가 발생했습니다");
    }
  }
}
</script>

<style scoped>
h1 {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 20px;
}
.form-card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: var(--shadow-card);
}
label {
  font-size: 13px;
  font-weight: 700;
  color: #4e5968;
  margin-top: 10px;
}
input,
textarea {
  padding: 14px 16px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 15px;
  outline: none;
  resize: vertical;
}
input:focus,
textarea:focus {
  border-color: var(--color-primary);
}
.btn-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}
</style>
