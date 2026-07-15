<script setup>
import { ref, computed } from 'vue'

import AppHeader from '../components/layout/AppHeader.vue'
import AppFooter from '../components/layout/AppFooter.vue'

import HeroSection from '../components/home/HeroSection.vue'
import TouristCarousel from '../components/home/TouristCarousel.vue'
import WeatherWidget from "../components/weather/WeatherWidget.vue";

import ChatbotButton from '../components/chatbot/ChatbotButton.vue'

import hanbatImage from '../assets/images/places/hanbat.jpg'
import expoImage from '../assets/images/places/expo.jpg'
import uamImage from '../assets/images/places/uam.jpg'

import { useI18n } from 'vue-i18n'

import daejeonLineImage from '../assets/images/backgrounds/daejeon-line.png'

const { t } = useI18n()

const touristSpots = computed(() => [
  {
    id: 1,
    name: t('places.hanbat.name'),
    category: t('places.category'),
    district: t('places.seogu'),
    description: t('places.hanbat.description'),
    imageUrl: hanbatImage
  },
  {
    id: 2,
    name: t('places.expo.name'),
    category: t('places.category'),
    district: t('places.yuseonggu'),
    description: t('places.expo.description'),
    imageUrl: expoImage
  },
  {
    id: 3,
    name: t('places.uam.name'),
    category: t('places.category'),
    district: t('places.donggu'),
    description: t('places.uam.description'),
    imageUrl: uamImage
  },
    {
    id: 4,
    name: t('places.daechung.name'),
    category: t('places.category'),
    district: t('places.daedeokgu'),
    description: t('places.daechung.description'),
    imageUrl: hanbatImage
  },
  {
    id: 5,
    name: t('places.yuseong.name'),
    category: t('places.category'),
    district: t('places.yuseonggu'),
    description: t('places.yuseong.description'),
    imageUrl: expoImage
  }
])
</script>


<template>
  <div class="home-view">

    <AppHeader />


    <main class="home-main">

      <!-- 메인 히어로 영역 -->
      <HeroSection />

      <!-- 관광지 카드 캐러셀 -->
      <TouristCarousel
        :spots="touristSpots"
      />

      <!-- 날씨 카드 -->
      <section class="home-weather">
        <WeatherWidget />
      </section>
    </main>
    <AppFooter />
    <ChatbotButton />
  </div>
</template>


<style scoped>
.home-view {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.home-main {
  width: 100%;
  flex: 1;
}

.home-weather {
  width: 100%;
  padding-bottom: 16px;
}

.home-view::before {
  position: absolute;
  right: -100px;
  bottom: 80px;
  width: 430px;
  height: 260px;
  background: radial-gradient(
    circle,
    rgba(233, 174, 86, 0.12),
    transparent 65%
  );
  content: "";
  pointer-events: none;
}

.daejeon-line-wrapper {
  width: 100%;
  margin-top: -10px;
  overflow: hidden;
}

.daejeon-line {
  width: 100%;
  height: 130px;
  object-fit: cover;
  object-position: center bottom;
  opacity: 0.35;
  pointer-events: none;
}

@media (max-width: 768px) {
  .daejeon-line {
    height: 80px;
  }
}
</style>