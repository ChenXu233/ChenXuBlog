// Auth route guard
export default defineNuxtRouteMiddleware((to, _from) => {
  const auth = useAuthStore()

  // Public routes that don't need auth
  const publicRoutes = ['/home', '/login', '/register', '/article', '/archive', '/friend', '/diary', '/warmos']
  const isPublic = publicRoutes.some(r => to.path === r || to.path.startsWith('/article/'))

  if (to.path.startsWith('/admin')) {
    if (!auth.isAuthenticated) {
      return navigateTo('/login?redirect=' + encodeURIComponent(to.fullPath))
    }
    if (!auth.isAdmin) {
      return navigateTo('/home')
    }
  } else if (to.path === '/login' || to.path === '/register') {
    // Already logged in, redirect to home
    if (auth.isAuthenticated) {
      return navigateTo('/home')
    }
  }
})