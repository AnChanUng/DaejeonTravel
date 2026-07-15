import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";

import BoardList from "../views/BoardList.vue";
import BoardDetail from "../views/BoardDetail.vue";
import BoardWrite from "../views/BoardWrite.vue";
import BoardEdit from "../views/BoardEdit.vue";

import LocationListView from "../views/LocationListView.vue";
import LocationDetailView from "../views/LocationDetailView.vue";

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

  // 관광지
  {
    path: "/tourist-spots",
    name: "tourist-spots",
    component: LocationListView,
    props: { type: "관광지" },
  },

  {
    path: "/tourist-spots/:id",
    name: "tourist-spot-detail",
    component: LocationDetailView,
  },

  // 음식점
  {
    path: "/restaurants",
    name: "restaurants",
    component: LocationListView,
    props: { type: "음식점" },
  },

  {
    path: "/restaurants/:id",
    name: "restaurant-detail",
    component: LocationDetailView,
  },

  // 숙박
  {
    path: "/accommodations",
    name: "accommodations",
    component: LocationListView,
    props: { type: "숙박" },
  },

  {
    path: "/accommodations/:id",
    name: "accommodation-detail",
    component: LocationDetailView,
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
    name: "board-list",
    component: BoardList,
  },

  {
    path: "/community/write",
    name: "board-write",
    component: BoardWrite,
  },

  {
    path: "/community/:id",
    name: "board-detail",
    component: BoardDetail,
  },

  {
    path: "/community/:id/edit",
    name: "board-edit",
    component: BoardEdit,
  },

  // 구 /board 주소 호환용 리다이렉트
  { path: "/board", redirect: "/community" },
  { path: "/board/write", redirect: "/community/write" },
  { path: "/board/:id", redirect: (to) => `/community/${to.params.id}` },
  {
    path: "/board/:id/edit",
    redirect: (to) => `/community/${to.params.id}/edit`,
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
