<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  spot: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <article class="tourist-card">
    <div class="tourist-card__content">
      <span class="tourist-card__badge">
        {{ spot.category }}
      </span>

      <h2 class="serif-title">
        {{ spot.name }}
      </h2>

      <div class="tourist-card__location">
        <span aria-hidden="true">📍</span>
        {{ spot.district }}
      </div>

      <p>
        {{ spot.description }}
      </p>

      <RouterLink
        :to="`/tourist-spots/${spot.id}`"
        class="tourist-card__detail-button"
      >
        {{ t('common.detail') }}
        <span aria-hidden="true">→</span>
      </RouterLink>
    </div>

    <div class="tourist-card__image-wrapper">
      <img
        :src="spot.imageUrl"
        :alt="`${spot.name} 관광지 사진`"
        class="tourist-card__image"
      >
    </div>
  </article>
</template>

<style scoped>
.tourist-card {
  min-height: 305px;

  display: grid;
  grid-template-columns: 34% 66%;

  overflow: hidden;

  background: var(--color-cream-100);
  border: 8px solid var(--color-cream-100);
  border-radius: 23px;
  box-shadow: 0 15px 35px rgba(74, 43, 20, 0.18);
}

.tourist-card__content {
  padding: 27px;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.tourist-card__badge {
  padding: 6px 11px;

  background: #c78927;
  border-radius: 999px;

  color: white;
  font-size: 13px;
  font-weight: 700;
}

.tourist-card h2 {
  margin-top: 16px;

  color: var(--color-brown-900);
  font-size: clamp(24px, 2vw, 31px);
}

.tourist-card__location {
  margin-top: 9px;

  display: flex;
  align-items: center;
  gap: 4px;

  color: #b36f18;
  font-size: 14px;
  font-weight: 700;
}

.tourist-card p {
  margin-top: 17px;

  color: var(--color-brown-700);
  font-size: 14px;
  line-height: 1.7;
}

.tourist-card__detail-button {
  margin-top: auto;
  padding: 10px 17px;

  display: inline-flex;
  align-items: center;
  gap: 8px;

  background: var(--color-gold-300);
  border-radius: 999px;

  color: var(--color-brown-900);
  font-size: 14px;
  font-weight: 800;
}

.tourist-card__detail-button:hover {
  background: var(--color-gold-400);
}

.tourist-card__image-wrapper {
  min-height: 290px;
  overflow: hidden;
}

.tourist-card__image {
  width: 100%;
  height: 100%;

  object-fit: cover;

  transition: transform 0.4s ease;
}

.tourist-card:hover .tourist-card__image {
  transform: scale(1.035);
}

@media (max-width: 720px) {
  .tourist-card {
    grid-template-columns: 1fr;
  }

  .tourist-card__image-wrapper {
    order: -1;
    min-height: 200px;
  }

  .tourist-card__content {
    min-height: 250px;
  }
}
</style>