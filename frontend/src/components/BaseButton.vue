<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary', // primary | ghost | danger
  },
})
</script>

<template>
  <button
    type="button"
    class="base-button"
    :class="`base-button--${variant}`"
  >
    <slot />
  </button>
</template>

<style scoped>
.base-button {
  padding: 12px 22px;
  border: 0;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease, transform 0.1s ease;
}

.base-button:active {
  transform: scale(0.97);
}

/* 메인 '자세히 보기' 버튼과 동일 계열 */
.base-button--primary {
  background: var(--color-gold-400);
  color: var(--color-brown-900);
  box-shadow: 0 6px 16px rgba(232, 165, 42, 0.3);
}

.base-button--primary:hover {
  background: var(--color-gold-500);
}

.base-button--ghost {
  background: transparent;
  color: var(--color-brown-700);
  border: 1.5px solid #dbb87e;
}

.base-button--ghost:hover {
  background: var(--color-cream-300);
}

.base-button--danger {
  background: #fdeeee;
  color: #c0392b;
  border: 1.5px solid #f0c4bf;
}

.base-button--danger:hover {
  background: #fbdddd;
}
</style>