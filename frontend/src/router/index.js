import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";

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
          display: inline-block;
          margin-top: 25px;
          padding: 10px 18px;
          background: #e8a52a;
          border-radius: 999px;
          color: #3f2819;
          text-decoration: none;
        "
      >
        메인으로 돌아가기
      </a>
    </main>
  `,
};

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/tourist-spots",
    component: TemporaryView,
  },
  {
    path: "/tourist-spots/:id",
    component: TemporaryView,
  },
  {
    path: "/restaurants",
    component: TemporaryView,
  },
  {
    path: "/accommodations",
    component: TemporaryView,
  },
  {
    path: "/festivals",
    component: TemporaryView,
  },
  {
    path: "/community",
    component: TemporaryView,
  },
  {
    path: "/community/:id",
    component: TemporaryView,
  },
  {
    path: "/search",
    component: TemporaryView,
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
