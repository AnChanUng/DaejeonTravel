<script setup>

const weather = {
  temp: 28,
  status: '맑음',
  rain: '10%',
  dust: '좋음'
}

</script>


<template>

<section class="weather-card">

  <div class="weather-title">
    ☀️ 오늘의 대전 여행 날씨
  </div>


  <div class="weather-content">


    <div class="weather-main">

      <span class="icon">
        🌤️
      </span>

      <strong>
        {{weather.temp}}°
      </strong>

      <span>
        {{weather.status}}
      </span>

    </div>



    <div class="weather-info">

      <span>
        💧 강수확률 {{weather.rain}}
      </span>

      <span>
        🌱 미세먼지 {{weather.dust}}
      </span>

    </div>


  </div>


</section>

</template>



<style scoped>

.weather-card {

 width:900px;

 margin:30px auto;

 padding:20px 35px;


 background:#fffaf0;

 border:1px solid #e8c98c;

 border-radius:20px;

}


.weather-title {

 font-size:20px;

 font-weight:700;

 color:#5b3518;

}


.weather-content {

 display:flex;

 justify-content:space-between;

 align-items:center;

 margin-top:15px;

}


.weather-main {

 display:flex;

 align-items:center;

 gap:15px;

}


.weather-main strong {

 font-size:45px;

}


.weather-info {

 display:flex;

 gap:25px;

 color:#806040;

}

</style>