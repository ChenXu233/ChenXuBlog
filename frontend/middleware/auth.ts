// Auth route guard
// SSR 阶段跳过（localStorage 不可用，token 由客户端 pinia persist 恢复后
// 由 client-side middleware 执行真正的检查）
export default defineNuxtRouteMiddleware((to, _from) => {
  const auth = useAuthStore();

  // Public routes that don't need auth
  const publicRoutes = [
    "/home",
    "/login",
    "/register",
    "/article",
    "/archive",
    "/friend",
    "/diary",
    "/warmos",
  ];
  const isPublic = publicRoutes.some(
    (r) => to.path === r || to.path.startsWith("/article/"),
  );

  // 服务端不检查（token 在客户端 localStorage）
  if (import.meta.server) {
    return;
  }

  if (to.path.startsWith("/admin")) {
    if (!auth.isAuthenticated) {
      return navigateTo("/login?redirect=" + encodeURIComponent(to.fullPath));
    }
    if (!auth.isAdmin) {
      return navigateTo("/home");
    }
  } else if (to.path === "/login" || to.path === "/register") {
    // Already logged in, redirect to home
    if (auth.isAuthenticated) {
      return navigateTo("/home");
    }
  }
});
