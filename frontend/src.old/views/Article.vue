<template>
  <div class="article-page">
    <BlossomCanvas />

    <section class="articles-section">
      <div class="articles-container">
        <BlogList title="最新文章" />
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";
import BlogList from "../components/BlogList.vue";
</script>

<style scoped>
.article-page {
  color: #fff;
  font-family: "JetBrains Mono", monospace;
  overflow-x: clip;
  cursor: none;
}

.article-page a,
.article-page button {
  cursor: none !important;
}

/* Articles Section */
.articles-section {
  position: relative;
  min-height: 100vh;
  padding: 8rem 10vw;
  z-index: 1;
}

.articles-container {
  max-width: 1400px;
  margin: 0 auto;
}
</style>