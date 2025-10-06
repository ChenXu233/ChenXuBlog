import { createRouter, createWebHashHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "home",
  },
  {
    path: "/home",
    name: "home",
    component: () => import("../views/Home.vue"),
    meta: {
      title: "首页",
      keepAlive: true,
      showAppBar: false, // 不显示AppBar
      showFooter: false, // 不显示Footer
    },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login.vue"),
    meta: {
      title: "登录",
      KeepAlive: true,
    },
  },
  {
    path: "/article",
    name: "article",
    component: () => import("../views/Article.vue"),
    meta: {
      title: "文章",
      KeepAlive: true,
    },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
