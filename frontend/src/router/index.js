import { createRouter, createWebHistory } from "vue-router";
import BoardList from "../views/BoardList.vue";
import BoardDetail from "../views/BoardDetail.vue";
import BoardWrite from "../views/BoardWrite.vue";
import BoardEdit from "../views/BoardEdit.vue";

const routes = [
  { path: "/", redirect: "/board" },
  { path: "/board", name: "BoardList", component: BoardList },
  { path: "/board/write", name: "BoardWrite", component: BoardWrite },
  { path: "/board/:id", name: "BoardDetail", component: BoardDetail },
  { path: "/board/:id/edit", name: "BoardEdit", component: BoardEdit },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
