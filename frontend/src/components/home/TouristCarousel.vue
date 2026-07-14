<script setup>
import {
  Autoplay,
  Navigation,
  Pagination
} from 'swiper/modules'

import {
  Swiper,
  SwiperSlide
} from 'swiper/vue'

import TouristCard from './TouristCard.vue'

import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

defineProps({
  spots: {
    type: Array,
    required: true
  }
})

const swiperModules = [
  Autoplay,
  Navigation,
  Pagination
]
</script>

<template>
  <section class="tourist-carousel">
    <Swiper
      :modules="swiperModules"
      :slides-per-view="1.45"
      :centered-slides="true"
      :space-between="26"
      :loop="spots.length >= 3"
      :navigation="true"
      :pagination="{
        clickable: true
      }"
      :autoplay="{
        delay: 4500,
        disableOnInteraction: false,
        pauseOnMouseEnter: true
      }"
      :breakpoints="{
        320: {
          slidesPerView: 1.04,
          spaceBetween: 12
        },
        750: {
          slidesPerView: 1.18,
          spaceBetween: 20
        },
        1100: {
          slidesPerView: 1.45,
          spaceBetween: 26
        }
      }"
      class="tourist-carousel__swiper"
    >
      <SwiperSlide
        v-for="spot in spots"
        :key="spot.id"
      >
        <TouristCard :spot="spot" />
      </SwiperSlide>
    </Swiper>
  </section>
</template>

<style scoped>
.tourist-carousel {
  position: relative;
  z-index: 10;

  width: min(1390px, 100%);
  margin: -36px auto 0;
  padding: 0 22px;
}

.tourist-carousel__swiper {
  padding: 15px 0 47px;
}

:deep(.swiper-slide) {
  opacity: 0.45;
  transform: scale(0.88);
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

:deep(.swiper-slide-active) {
  z-index: 2;
  opacity: 1;
  transform: scale(1);
}

:deep(.swiper-button-prev),
:deep(.swiper-button-next) {

  width:46px;
  height:46px;


  background:rgba(255,250,240,0.95);


  border:1px solid #e8c98c;


  border-radius:50%;


  box-shadow:
  0 4px 12px rgba(120,80,30,0.12);


  color:#8a6234;


  transition:all .2s ease;

}



:deep(.swiper-button-prev:hover),
:deep(.swiper-button-next:hover) {


  background:#f5bd45;


  color:white;


  transform:scale(1.08);

}



:deep(.swiper-button-prev::after),
:deep(.swiper-button-next::after) {


  font-size: 10px;

  font-weight: 400; 


}

:deep(.swiper-pagination-bullet) {
  width: 9px;
  height: 9px;

  background: #d9c6a9;
  opacity: 1;
}

:deep(.swiper-pagination-bullet-active) {
  background: var(--color-gold-500);
}

@media (max-width: 650px) {
  .tourist-carousel {
    margin-top: -25px;
    padding: 0 12px;
  }

  :deep(.swiper-button-prev),
  :deep(.swiper-button-next) {
    display: none;
  }
}
</style>