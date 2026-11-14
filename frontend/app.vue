<template>
  <div id="app">
    <NuxtRouteAnnouncer />
    <NuxtLoadingIndicator color="var(--cx-accent)" :height="2" />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <MouseTrail />
    <DockBar />
    <UToaster />
  </div>
</template>

<script setup lang="ts">
// 恢复登录态（仅浏览器；服务端没有 localStorage）
const auth = useAuthStore();
if (import.meta.client && auth.token) {
  auth.fetchUserInfo();
  auth.fetchPermissions();
}
</script>
