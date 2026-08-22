<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">仪表盘</h2>

    <!-- Stats cards -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
      <UCard v-for="card in statCards" :key="card.label">
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-lg bg-primary-50 dark:bg-primary-500/10">
            <UIcon :name="card.icon" class="w-5 h-5 text-primary-500" />
          </div>
          <div>
            <div class="text-2xl font-bold">{{ card.value }}</div>
            <div class="text-sm text-gray-500">{{ card.label }}</div>
          </div>
        </div>
      </UCard>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <!-- Recent blogs -->
      <UCard>
        <template #header>
          <div class="font-semibold">最近文章</div>
        </template>
        <ul class="space-y-3">
          <li
            v-for="blog in stats?.recent_blogs || []"
            :key="blog.id"
            class="flex justify-between items-center"
          >
            <NuxtLink
              :to="`/article/${blog.id}`"
              class="hover:text-primary-500 truncate"
              >{{ blog.title }}</NuxtLink
            >
            <UBadge
              :color="blog.published ? 'success' : 'warning'"
              variant="soft"
            >
              {{ blog.published ? "已发布" : "草稿" }}
            </UBadge>
          </li>
          <li v-if="!stats?.recent_blogs?.length" class="text-gray-400 text-sm">
            暂无文章
          </li>
        </ul>
      </UCard>

      <!-- Recent comments -->
      <UCard>
        <template #header>
          <div class="font-semibold">最近评论</div>
        </template>
        <ul class="space-y-3">
          <li
            v-for="comment in stats?.recent_comments || []"
            :key="comment.id"
            class="text-sm"
          >
            <span class="text-gray-500">{{ comment.username }}：</span>
            <span class="line-clamp-1">{{ comment.content }}</span>
          </li>
          <li
            v-if="!stats?.recent_comments?.length"
            class="text-gray-400 text-sm"
          >
            暂无评论
          </li>
        </ul>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" });

import { adminService } from "~/service/admin";
import type { AdminStatsResponse } from "~/src/client/types.gen";

const stats = ref<AdminStatsResponse | null>(null);
const loadError = ref("");

// 客户端加载（token 由 pinia persist 恢复后才可用）
async function loadStats() {
  if (!useAuthStore().token) return;
  try {
    stats.value = await adminService.getStats();
  } catch (e: any) {
    loadError.value = e?.message || "加载失败";
    if (e?.status === 401) {
      useAuthStore().logout();
    }
  }
}

onMounted(loadStats);
if (import.meta.client && useAuthStore().token) {
  // 客户端直接导航时立即加载
  await loadStats();
}

const statCards = computed(() => [
  {
    label: "用户总数",
    value: stats.value?.total_users ?? 0,
    icon: "i-heroicons-users",
  },
  {
    label: "文章总数",
    value: stats.value?.total_blogs ?? 0,
    icon: "i-heroicons-document-text",
  },
  {
    label: "评论总数",
    value: stats.value?.total_comments ?? 0,
    icon: "i-heroicons-chat-bubble-left-right",
  },
  {
    label: "今日文章",
    value: stats.value?.total_blogs_today ?? 0,
    icon: "i-heroicons-calendar-days",
  },
]);
</script>
