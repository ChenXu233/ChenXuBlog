<template>
  <div id="app">
    <LoadingOverlay :show="loading" />
    <AppBar v-if="$route.meta.showAppBar !== false" />
    <router-view v-slot="{ Component }">
      <transition>
        <component :is="Component" :key="$route.path" />
      </transition>
    </router-view>
    <Footer v-if="$route.meta.showFooter !== false" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { nextTick } from "vue";
import AppBar from "./components/AppBar.vue";
import Footer from "./components/Footer.vue";
import LoadingOverlay from "./components/LoadingOverlay.vue";

const route = useRoute();
const loading = ref(false);

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
