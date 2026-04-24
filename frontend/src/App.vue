<template>
  <div id="app" class="app-wrapper">
    <div class="noise-overlay"></div>
    <LoadingOverlay :show="loading" />
    <MouseTrail v-if="!inIframe" />
    <router-view v-slot="{ Component }" class="app-content">
      <transition name="fade" mode="out-in">
        <component :is="Component" :key="$route.path" />
      </transition>
    </router-view>
    <DockBar
      v-if="!isWarmOSRoute && !inIframe && $route.meta.showDockBar !== false"
      class="app-bottom"
    />
    <Footer
      v-if="$route.meta.showFooter !== false && !isWarmOSRoute && !inIframe"
      class="app-bottom"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { useRoute } from "vue-router";
import { nextTick } from "vue";
import Footer from "./components/Footer.vue";
import DockBar from "./components/WarmOS/DockBar.vue";
import LoadingOverlay from "./components/LoadingOverlay.vue";
import MouseTrail from "./components/effects/MouseTrail.vue";

const route = useRoute();
const loading = ref(false);

const isWarmOSRoute = computed(() => {
  return route.path.startsWith("/warmos") || route.name === "WarmOS";
});

const inIframe = computed(() => {
  try {
    return window.self !== window.top;
  } catch (e) {
    return true;
  }
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
</script>
<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s;
}
.app-content {
  flex: 1;
}
.app-bottom {
  margin-top: auto;
}
</style>

<style>
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
