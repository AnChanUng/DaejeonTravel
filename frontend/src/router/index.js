import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";

import BoardList from "../views/BoardList.vue";
import BoardDetail from "../views/BoardDetail.vue";
import BoardWrite from "../views/BoardWrite.vue";
import BoardEdit from "../views/BoardEdit.vue";
import BoardBookmarks from "../views/BoardBookmarks.vue";

import LocationListView from "../views/LocationListView.vue";
import LocationDetailView from "../views/LocationDetailView.vue";
import FestivalCalendarView from "../views/FestivalCalendarView.vue";
import MapView from "../views/MapView.vue";
import DashboardView from "../views/DashboardView.vue";

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

  // 축제 캘린더
  {
    path: "/festivals",
    name: "festivals",
    component: FestivalCalendarView,
  },

  // 여행 지도 (핀 표시 + 경로 안내)
  {
    path: "/map",
    name: "map",
    component: MapView,
  },

  // 통계 대시보드
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
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

  // 주의: 동적 라우트(/community/:id)보다 반드시 위에 있어야
  // "bookmarks"가 게시글 id로 오인되지 않는다.
  {
    path: "/community/bookmarks",
    name: "board-bookmarks",
    component: BoardBookmarks,
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
