<template>
  <!-- 复用创建页组件（内部通过 route.params.id 判断编辑态） -->
  <ArticleEditor />
</template>

<script setup lang="ts">
import ArticleEditor from "../create.vue";
</script>
