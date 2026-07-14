<template>
  <div v-if="post">
    <button class="back" @click="$router.push('/board')">‹ 목록으로</button>

    <div class="detail-card">
      <span class="badge">{{ post.category }}</span>
      <h1>{{ post.title }}</h1>
      <p class="date">{{ formatDate(post.created_at) }}</p>
      <hr />
      <p class="content">{{ post.content }}</p>
    </div>

    <div class="btn-row">
      <BaseButton variant="ghost" @click="openModal('edit')">수정</BaseButton>
      <BaseButton variant="danger" @click="openModal('delete')"
        >삭제</BaseButton
      >
    </div>

    <div v-if="showModal" class="modal-bg" @click.self="showModal = false">
      <div class="modal">
        <h2>비밀번호 확인</h2>
        <input
          v-model="password"
          type="password"
          placeholder="수정용 비밀번호 입력"
          @keyup.enter="confirm"
          autofocus
        />
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
        <BaseButton class="full" @click="confirm">확인</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../api";
import BaseButton from "../components/BaseButton.vue";

const route = useRoute();
const router = useRouter();
const post = ref(null);

const showModal = ref(false);
const mode = ref("");
const password = ref("");
const errorMsg = ref("");

async function fetchPost() {
  const res = await api.get(`/api/posts/${route.params.id}`);
  post.value = res.data;
}

function openModal(m) {
  mode.value = m;
  password.value = "";
  errorMsg.value = "";
  showModal.value = true;
}

async function confirm() {
  if (!password.value) {
    errorMsg.value = "비밀번호를 입력해주세요";
    return;
  }

  if (mode.value === "delete") {
    try {
      await api.delete(`/api/posts/${route.params.id}`, {
        data: { password: password.value },
      });
      alert("삭제되었습니다");
      router.push("/board");
    } catch (e) {
      errorMsg.value =
        e.response?.status === 403
          ? "비밀번호가 일치하지 않습니다"
          : "오류가 발생했습니다";
    }
  } else {
    sessionStorage.setItem("editPw", password.value);
    router.push(`/board/${route.params.id}/edit`);
  }
}

function formatDate(dt) {
  return dt ? dt.slice(0, 10).replaceAll("-", ".") : "";
}

onMounted(fetchPost);
</script>

<style scoped>
.back {
  background: none;
  color: var(--color-text-sub);
  font-size: 14px;
  margin-bottom: 12px;
}
.detail-card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 28px;
  box-shadow: var(--shadow-card);
}
.badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary);
  background: #e8f1fe;
  border-radius: 8px;
  padding: 3px 8px;
  margin-bottom: 10px;
}
h1 {
  font-size: 22px;
  font-weight: 800;
}
.date {
  color: var(--color-text-sub);
  font-size: 13px;
  margin-top: 6px;
}
hr {
  border: none;
  border-top: 1px solid var(--color-bg);
  margin: 18px 0;
}
.content {
  font-size: 15px;
  white-space: pre-wrap;
}

.btn-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}

.modal-bg {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 28px;
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.modal h2 {
  font-size: 18px;
  font-weight: 800;
  text-align: center;
}
.modal input {
  padding: 14px 16px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 15px;
  outline: none;
}
.modal input:focus {
  border-color: var(--color-primary);
}
.error {
  color: var(--color-danger);
  font-size: 13px;
}
.full {
  width: 100%;
}
</style>
