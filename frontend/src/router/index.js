import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";

import BoardList from "../views/BoardList.vue";
import BoardDetail from "../views/BoardDetail.vue";
import BoardWrite from "../views/BoardWrite.vue";
import BoardEdit from "../views/BoardEdit.vue";

const TemporaryView = {
  template: `
    <main style="
      min-height: 100vh;
      padding: 80px 20px;
      text-align: center;
      background: #fff9ed;
    ">
      <h1>페이지 준비 중입니다.</h1>

      <p style="margin-top: 15px;">
        현재는 메인 페이지를 먼저 구현하고 있습니다.
      </p>

      <a
        href="/"
        style="
          display:inline-block;
          margin-top:25px;
          padding:10px 18px;
          background:#e8a52a;
          border-radius:999px;
          color:#3f2819;
          text-decoration:none;
        "
      >
        메인으로 돌아가기
      </a>

    </main>
  `,
};

const routes = [
  // 메인
  {
    path: "/",
    name: "home",
    component: HomeView,
  },

  // 관광
  {
    path: "/tourist-spots",
    component: TemporaryView,
  },

  {
    path: "/tourist-spots/:id",
    component: TemporaryView,
  },

  // 음식점
  {
    path: "/restaurants",
    component: TemporaryView,
  },

  // 숙박
  {
    path: "/accommodations",
    component: TemporaryView,
  },

  // 축제
  {
    path: "/festivals",
    component: TemporaryView,
  },

  // 검색
  {
    path: "/search",
    component: TemporaryView,
  },

  // 커뮤니티
  {
    path: "/community",
    component: BoardList,
  },

  {
    path: "/community/write",
    component: BoardWrite,
  },

  {
    path: "/community/:id",
    component: BoardDetail,
  },

  {
    path: "/community/:id/edit",
    component: BoardEdit,
  },
];

const router = createRouter({
  history: createWebHistory(),

  routes,

  scrollBehavior() {
    return {
      top: 0,
    };
  },
});

export default router;
