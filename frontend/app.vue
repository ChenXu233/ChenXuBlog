<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <DockBar />
    <UToaster />
  </div>
</template>

<script setup lang="ts">
// Initialize auth state from persisted storage on app mount
const auth = useAuthStore();
if (auth.token) {
  auth.fetchUserInfo();
  auth.fetchPermissions();
}
</script>
