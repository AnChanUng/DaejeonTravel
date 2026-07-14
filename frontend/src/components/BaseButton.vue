<template>
  <button :class="['base-btn', variant]" v-bind="$attrs">
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: { type: String, default: "primary" }, // primary | ghost | danger
});
</script>

<style scoped>
.base-btn {
  padding: 13px 24px;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 700;
  transition: filter 0.15s;
}
.base-btn:hover {
  filter: brightness(0.94);
}
.primary {
  background: var(--color-primary);
  color: #fff;
}
.ghost {
  background: var(--color-bg);
  color: #4e5968;
}
.danger {
  background: #fff0f0;
  color: var(--color-danger);
}
</style>
