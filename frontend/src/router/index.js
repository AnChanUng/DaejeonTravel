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

  // 검색
  {
    path: "/search",
    name: "search",
    component: LocationListView,
    props: { type: "검색" },
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
