<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import kkumdoriImage from '@/assets/images/mascots/kkumdori.png'
import kkumsuniImage from '@/assets/images/mascots/kkumsuni.png'
import bakeryImage from '@/assets/images/backgrounds/bakery-left.png'
import daejeonRightImage from '@/assets/images/backgrounds/daejeon-right.png'


const router = useRouter()

const keyword = ref('')


const handleSearch = () => {

  const value = keyword.value.trim()

  if (!value) {
    return
  }


  router.push({
    path:'/search',
    query:{
      keyword:value
    }
  })

}

</script>



<template>

<section class="hero-section">


  <div class="hero-section__inner">


    <!-- 성심당 배경 -->
    <div
      class="hero-section__bakery"
      :style="{
        backgroundImage:`url(${bakeryImage})`
      }"
    />



    <!-- 배경 패턴 -->
    <div class="hero-section__pattern" />



    <!-- 꿈돌이 -->
    <img
      :src="kkumdoriImage"
      alt="꿈돌이"
      class="hero-section__mascot hero-section__mascot--left"
    />



    <!-- 중앙 -->
    <div class="hero-section__content">


      <span class="hero-section__bread">
        🥐
      </span>


      <h1>
        대전의 맛과 여행을 한눈에
      </h1>


      <p>
        관광지, 음식점, 숙박 정보를 쉽고 빠르게 찾아보세요!
      </p>



      <form
        class="hero-section__search"
        @submit.prevent="handleSearch"
      >

        <input
          v-model="keyword"
          type="search"
          placeholder="장소 이름을 검색해보세요. 예: 한밭수목원, 유성온천"
        />



        <button>
          🔍
        </button>


      </form>


    </div>




    <!-- 꿈순이 -->
    <img
      :src="kkumsuniImage"
      alt="꿈순이"
      class="hero-section__mascot hero-section__mascot--right"
    />




    <!-- Daejeon 배경 -->
    <img
      :src="daejeonRightImage"
      alt="Daejeon is U"
      class="hero-section__daejeon"
    />


  </div>


</section>


</template>





<style scoped>


.hero-section {


  position:relative;


  width:100%;


  height:430px;


  overflow:hidden;


}





/*
  모든 요소 기준점
*/

.hero-section__inner {


  position:relative;


  width:1600px;


  height:430px;


  margin:0 auto;


}







/* ===================
   배경
=================== */



.hero-section__bakery {


  position:absolute;


  left:0;


  top:0;



  width:504px;


  height:408px;



  background-repeat:no-repeat;


  background-position:left top;


  background-size:contain;



  opacity:0.4;


  z-index:1;


}







.hero-section__daejeon {


  position:absolute;


  right:0;


  top:0;



  width:433px;


  height:449px;



  object-fit:contain;



  opacity:0.3;



  filter:

    brightness(1.1)

    saturate(65%);



  z-index:1;


}






.hero-section__pattern {


  position:absolute;


  inset:0;



  background-image:

  linear-gradient(
    90deg,
    rgba(230,169,78,.08) 1px,
    transparent 1px
  ),

  linear-gradient(
    rgba(230,169,78,.08) 1px,
    transparent 1px
  );



  background-size:120px 120px;


}







/* ===================
   캐릭터
=================== */


.hero-section__mascot {


  position:absolute;


  bottom:30px;



  width:240px;


  z-index:5;


}







.hero-section__mascot--left {


  left:300px;


}







.hero-section__mascot--right {


  right:300px;


}








/* ===================
   중앙
=================== */


.hero-section__content {


  position:absolute;


  top:70px;


  left:50%;



  transform:translateX(-50%);



  width:670px;



  text-align:center;



  z-index:10;


}





.hero-section__bread {


  display:block;


  font-size:32px;


}





.hero-section h1 {


  margin-top:5px;


  color:#4b2b16;



  font-size:56px;


  font-weight:800;



  letter-spacing:-0.05em;


}





.hero-section p {


  margin-top:10px;


  color:#76553a;


  font-size:17px;


}








/* ===================
   검색
=================== */


.hero-section__search {


  width:100%;


  height:65px;


  margin-top:20px;



  padding:

  7px 8px 7px 20px;



  display:flex;


  align-items:center;


  gap:12px;



  background:white;


  border:1px solid #d7af6f;


  border-radius:999px;



  box-shadow:

  0 10px 25px rgba(91,57,21,.15);


}






.search-icon {


  font-size:26px;


}





.hero-section__search input {


  flex:1;


  border:0;


  outline:0;


  font-size:15px;


}






.hero-section__search button {


  width:51px;


  height:51px;



  border:0;


  border-radius:50%;



  background:#f5bd45;


}








/* ===================
   화면 대응
=================== */


@media(max-width:1600px){


  .hero-section__inner{


    transform:scale(
      calc(100vw / 1600)
    );


    transform-origin:top center;


  }


}



@media(max-width:900px){


  .hero-section__inner{


    transform:none;


    width:100%;


  }



  .hero-section__bakery,

  .hero-section__daejeon{


    display:none;


  }



  .hero-section__mascot{


    opacity:.3;


  }


}

</style>