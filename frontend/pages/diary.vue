<template>
  <div class="diary-page">
    <BlossomCanvas />

    <section class="diary-section">
      <h1>随谈</h1>
      <p>抛开代码架构，回归纯粹的片语轻言。</p>
    </section>
  </div>
</template>

<script setup lang="ts">
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";
</script>

<style scoped>
.diary-page {
  color: #fff;
  font-family: "JetBrains Mono", monospace;
  overflow-x: clip;
  cursor: none;
  min-height: 100vh;
}

.diary-section {
  padding: 8rem 10vw;
  text-align: center;
}

.diary-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.diary-section p {
  color: #aaa;
  font-size: 1.2rem;
}
</style>
