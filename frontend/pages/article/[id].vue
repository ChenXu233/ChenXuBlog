<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <div v-if="article">
        <h1 class="text-4xl font-bold mb-4">{{ article.title }}</h1>
        <div class="text-gray-500 mb-8">{{ article.created_at }} · {{ article.view_count }} 次阅读</div>
        <div class="prose dark:prose-invert max-w-none" v-html="renderedBody"></div>
      </div>
      <div v-else class="text-center py-20">
        <p class="text-gray-500">文章不存在</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Article } from '~/types/article'
import markdownit from 'markdown-it'

const md = markdownit()
const route = useRoute()
const { data } = await useFetch<Article>(`/apis/v1/blog/${route.params.id}`)
const article = data.value
const renderedBody = computed(() => article.value ? md.render(article.value.body) : '')
</script>