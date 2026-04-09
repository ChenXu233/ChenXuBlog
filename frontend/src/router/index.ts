import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import { useTokenStore } from "../stores/token";
import { usePermissionStore } from "../stores/permission";
import { permissionService } from "../service/permission";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/home",
    name: "home",
    component: () => import("../views/Home.vue"),
    meta: {
      title: "首页",
      keepAlive: true,
      showFooter: false,
      transition: "slide-right",
    },
  },
  {
    path: "/warmos",
    name: "warmos",
    component: () => import("../views/WarmOS/index.vue"),
    meta: {
      title: "Warmos",
      keepAlive: true,
      showFooter: false,
    }
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login.vue"),
    meta: {
      title: "登录",
      keepAlive: true,
      transition: "slide-right",
    },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Register.vue"),
    meta: {
      title: "注册",
      keepAlive: true,
      transition: "slide-right",
    },
  },
  {
    path: "/article",
    name: "article",
    component: () => import("../views/Article.vue"),
    meta: {
      title: "文章列表",
      keepAlive: true,
      transition: "slide-right",
    },
  },
  {
    path: "/article/:id",
    name: "article-detail",
    component: () => import("../views/ArticleDetail.vue"),
    meta: {
      title: "文章详情",
      keepAlive: true,
      transition: "slide-right",
    },
  },
  {
    path: "/article/create",
    name: "article-create",
    component: () => import("../views/ArticleEditor.vue"),
    meta: {
      title: "创建文章",
      requiresAuth: true,
      requiresPermission: "blog:create",
      transition: "slide-right",
    },
  },
  {
    path: "/article/edit/:id",
    name: "article-edit",
    component: () => import("../views/ArticleEditor.vue"),
    meta: {
      title: "编辑文章",
      requiresAuth: true,
      transition: "slide-right",
    },
  },
  {
    path: "/user/:id",
    name: "user-profile",
    component: () => import("../views/UserProfile.vue"),
    meta: {
      title: "用户中心",
      transition: "slide-right",
    },
  },
  {
    path: "/archive",
    name: "archive",
    component: () => import("../views/Archive.vue"),
    meta: {
      title: "归档",
      transition: "slide-right",
    },
  },
  {
    path: "/friend",
    name: "friend",
    component: () => import("../views/Friend.vue"),
    meta: {
      title: "友链",
      transition: "slide-right",
    },
  },
  {
    path: "/diary",
    name: "diary",
    component: () => import("../views/Diary.vue"),
    meta: {
      title: "随谈",
      transition: "slide-right",
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

let permissionLoaded = false;

const loadPermissions = async () => {
  if (permissionLoaded) return;
  const tokenStore = useTokenStore();
  const permissionStore = usePermissionStore();

  if (!tokenStore.isAuthenticated) {
    permissionLoaded = false;
    return;
  }

  try {
    const res = await permissionService.getPermissions();
    permissionStore.setPermissions(res.permissions);
    permissionLoaded = true;
  } catch {
    permissionLoaded = false;
  }
};

router.beforeEach(async (to, _from, next) => {
  const tokenStore = useTokenStore();
  const permissionStore = usePermissionStore();

  // 需要认证的路由
  if (to.meta.requiresAuth && !tokenStore.isAuthenticated) {
    next({ name: "login", query: { redirect: to.fullPath } });
    return;
  }

  // 已登录用户访问登录页，重定向到首页
  if (to.name === "login" && tokenStore.isAuthenticated) {
    next({ name: "home" });
    return;
  }

  // 需要权限的路由
  if (to.meta.requiresPermission) {
    await loadPermissions();
    if (!permissionStore.hasPermission(to.meta.requiresPermission as string)) {
      alert("您没有权限执行此操作");
      next({ name: "home" });
      return;
    }
  }

  next();
});

// 登录成功后重置权限状态
export const resetPermissionState = () => {
  permissionLoaded = false;
};

export default router;
