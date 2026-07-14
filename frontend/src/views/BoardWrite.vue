<template>
  <div>
    <h1>게시글 작성</h1>

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
        <BaseButton variant="ghost" @click="$router.back()">취소</BaseButton>
        <BaseButton @click="submit">등록</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";
import api from "../api";
import BaseButton from "../components/BaseButton.vue";

const router = useRouter();
const form = reactive({
  category: "관광지",
  title: "",
  content: "",
  password: "",
});

async function submit() {
  if (!form.title.trim()) return alert("제목을 입력해주세요");
  if (!form.content.trim()) return alert("내용을 입력해주세요");
  if (!form.password.trim()) return alert("비밀번호를 입력해주세요");

  const res = await api.post("/api/posts", form);
  router.push(`/board/${res.data.id}`);
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
textarea,
select {
  padding: 14px 16px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 15px;
  outline: none;
  background: var(--color-card);
  resize: vertical;
}
input:focus,
textarea:focus,
select:focus {
  border-color: var(--color-primary);
}
.hint {
  font-size: 12px;
  color: var(--color-text-sub);
}
.btn-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}
</style>
