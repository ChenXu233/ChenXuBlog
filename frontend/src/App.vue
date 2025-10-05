<template>
  <div id="app">
    <AppBar />
    <router-view />
    <Footer />
  </div>
</template>

<script setup lang="ts">
import AppBar from "./components/AppBar.vue";
import Footer from "./components/Footer.vue";
</script>
