<script setup>
import { ref } from 'vue'

import AppHeader from '../components/layout/AppHeader.vue'
import AppFooter from '../components/layout/AppFooter.vue'

import HeroSection from '../components/home/HeroSection.vue'
import TouristCarousel from '../components/home/TouristCarousel.vue'
import WeatherCard from '../components/home/WeatherCard.vue'

import ChatbotButton from '../components/chatbot/ChatbotButton.vue'

import hanbatImage from '../assets/images/places/hanbat.jpg'
import expoImage from '../assets/images/places/expo.jpg'
import uamImage from '../assets/images/places/uam.jpg'

import daejeonLineImage from '../assets/images/backgrounds/daejeon-line.png'


const touristSpots = ref([
  {
    id: 1,
    name: '한밭수목원',
    category: '관광지',
    district: '서구',
    description:
      '사계절 아름다운 자연을 만날 수 있는 도심 속 힐링 공간',
    imageUrl: hanbatImage
  },
  {
    id: 2,
    name: '엑스포시민광장',
    category: '관광지',
    district: '유성구',
    description:
      '한빛탑과 엑스포다리를 함께 볼 수 있는 대전의 대표 공간',
    imageUrl: expoImage
  },
  {
    id: 3,
    name: '우암사적공원',
    category: '관광지',
    district: '동구',
    description:
      '역사적인 건축물과 아름다운 자연이 어우러진 전통문화 공간',
    imageUrl: uamImage
  },
  {
    id: 4,
    name: '대청호 오백리길',
    category: '관광지',
    district: '대덕구',
    description:
      '대청호의 풍경을 따라 걷는 대전 대표 생태 탐방길',
    imageUrl: hanbatImage
  },
  {
    id: 5,
    name: '유성온천',
    category: '관광지',
    district: '유성구',
    description:
      '대전을 대표하는 온천 관광지에서 편안한 휴식을 즐겨보세요',
    imageUrl: expoImage
  }
])


const recentPosts = ref([
  {
    id: 1,
    title: '성심당 신상 빵 먹어봤어요! 역시 명불허전',
    createdAt: '07.14'
  },
  {
    id: 2,
    title: '대청호 오백리길 걷기 좋은 코스 추천드립니다',
    createdAt: '07.13'
  },
  {
    id: 3,
    title: '유성온천에서 힐링하고 왔어요',
    createdAt: '07.12'
  },
  {
    id: 4,
    title: '이번 주말 부모님과 갈 만한 곳이 있을까요?',
    createdAt: '07.11'
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
      <WeatherCard />

      <!-- 대전 라인 장식 -->
      <div class="daejeon-line-wrapper">

        <img
          :src="daejeonLineImage"
          alt="대전 랜드마크"
          class="daejeon-line"
        />

      </div>


    </main>


    <AppFooter />


    <ChatbotButton />

  </div>
</template>


<style scoped>

.home-view {

  width:100%;

  height:100vh;

  display:flex;

  flex-direction:column;

  overflow:hidden;
}

.home-main {

   flex:1;

  display:flex;

  flex-direction:column;

  justify-content:flex-start;

  align-items:center;

  overflow:hidden;

}

.home-main :deep(.hero-section) {

  flex-shrink:0;

}



.home-view::before {

  position: absolute;

  right: -100px;

  bottom: 80px;


  width: 430px;

  height: 260px;


  background:
    radial-gradient(
      circle,
      rgba(233,174,86,0.12),
      transparent 65%
    );


  content: '';

  pointer-events: none;

}



/* 대전 랜드마크 라인 */

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



@media(max-width:768px){

  .daejeon-line {

    height:80px;

  }

}

</style>