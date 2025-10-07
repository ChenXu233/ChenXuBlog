import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/home", // 修复：确保重定向路径是字符串
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
      keepAlive: true,
    },
  },
  {
    path: "/article",
    name: "article",
    component: () => import("../views/Article.vue"),
    meta: {
      title: "文章",
      keepAlive: true,
    },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Register.vue"),
    meta: {
      title: "注册",
      keepAlive: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
