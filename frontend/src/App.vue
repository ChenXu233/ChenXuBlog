<template>
  <div id="app">
    <AppBar v-if="$route.meta.showAppBar !== false" />
    <router-view />
    <Footer v-if="$route.meta.showFooter !== false" />
  </div>
</template>

<script setup lang="ts">
import AppBar from "./components/AppBar.vue";
import Footer from "./components/Footer.vue";
</script>
