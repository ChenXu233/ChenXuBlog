<template>
  <div id="app">
    <LoadingOverlay :show="loading" />
    <MouseTrail />
    <NuxtRouteAnnouncer />
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <DockBar />
    <Footer v-if="!hideFooter" />
    <UToaster />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

const route = useRoute();
const loading = ref(false);

// 原版: Footer 通过 route.meta.showFooter 控制；Nuxt 里按路径判断
const hideFooter = computed(() => {
  const p = route.path;
  return p === "/home" || p === "/login" || p === "/register";
});

watch(
  () => route.path,
  async () => {
    loading.value = true;
    await nextTick();
    setTimeout(() => {
      loading.value = false;
    }, 300);
  },
);

// Initialize auth state from persisted storage on app mount
const auth = useAuthStore();
if (auth.token) {
  auth.fetchUserInfo();
  auth.fetchPermissions();
}
</script>
