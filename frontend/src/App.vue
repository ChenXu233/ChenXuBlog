<template>
  <div id="app">
    <LoadingOverlay :show="loading" />
    <MouseTrail />
    <router-view v-slot="{ Component }">
      <transition>
        <component :is="Component" :key="$route.path" />
      </transition>
    </router-view>
    <DockBar v-if="!isWarmOSRoute && !inIframe" />
    <Footer v-if="$route.meta.showFooter !== false && !isWarmOSRoute && !inIframe" />
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
  return route.path.startsWith('/warmos') || route.name === 'WarmOS';
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
