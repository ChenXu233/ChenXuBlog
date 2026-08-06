<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <div class="max-w-6xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-8">文章列表</h1>
      <div class="grid gap-6 md:grid-cols-2">
        <UCard v-for="article in articles" :key="article.id" class="hover:shadow-lg transition-shadow">
          <NuxtLink :to="`/article/${article.id}`">
            <h2 class="text-xl font-semibold mb-2">{{ article.title }}</h2>
            <p class="text-gray-500 dark:text-gray-400 text-sm mb-4">{{ article.created_at }}</p>
            <div class="flex gap-2">
              <UBadge v-for="tag in article.tags_name" :key="tag" variant="soft">{{ tag }}</UBadge>
            </div>
          </NuxtLink>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ArticleList } from '~/types/article'

const { data } = await useFetch<ArticleList>('/apis/v1/blog/')
const articles = data.value?.items || []
</script>