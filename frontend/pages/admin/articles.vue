<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">文章管理</h2>

    <UCard>
      <div class="flex justify-between items-center mb-4">
        <div class="flex gap-2">
          <UButton
            :variant="publishedFilter === null ? 'solid' : 'ghost'"
            size="sm"
            @click="setFilter(null)"
            >全部</UButton
          >
          <UButton
            :variant="publishedFilter === true ? 'solid' : 'ghost'"
            size="sm"
            color="success"
            @click="setFilter(true)"
            >已发布</UButton
          >
          <UButton
            :variant="publishedFilter === false ? 'solid' : 'ghost'"
            size="sm"
            color="warning"
            @click="setFilter(false)"
            >草稿</UButton
          >
        </div>
      </div>

      <UTable :data="articles" :columns="columns" :loading="pending">
        <template #published-cell="{ row }">
          <UBadge
            :color="row.original.published ? 'success' : 'warning'"
            variant="soft"
          >
            {{ row.original.published ? "已发布" : "草稿" }}
          </UBadge>
        </template>
        <template #view_count-cell="{ row }">
          <span class="text-sm text-gray-500">{{
            row.original.view_count
          }}</span>
        </template>
        <template #actions-cell="{ row }">
          <div class="flex gap-1">
            <UButton
              icon="i-heroicons-eye"
              size="xs"
              variant="ghost"
              :to="`/article/${row.original.id}`"
            />
            <UButton
              icon="i-heroicons-paper-airplane"
              size="xs"
              variant="ghost"
              :color="row.original.published ? 'warning' : 'success'"
              @click="togglePublish(row.original)"
            />
            <UButton
              icon="i-heroicons-trash"
              size="xs"
              variant="ghost"
              color="error"
              @click="deleteArticle(row.original)"
            />
          </div>
        </template>
      </UTable>

      <div class="flex justify-center mt-4">
        <UPagination v-model="page" :page-count="pageSize" :total="total" />
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth", ssr: false });

import { adminService } from "~/service/admin";
import type { AdminBlogResponse } from "~/src/client/types.gen";

const page = ref(1);
const pageSize = 10;
const publishedFilter = ref<boolean | null>(null);

const columns = [
  { accessorKey: "id", header: "ID" },
  { accessorKey: "title", header: "标题" },
  { accessorKey: "username", header: "作者" },
  { accessorKey: "published", header: "状态" },
  { accessorKey: "view_count", header: "阅读" },
  { accessorKey: "actions", header: "操作" },
];

const data = ref<Awaited<ReturnType<typeof adminService.getBlogs>> | null>(
  null,
);
const pending = ref(false);

async function load() {
  pending.value = true;
  try {
    data.value = await adminService.getBlogs(
      page.value,
      pageSize,
      publishedFilter.value,
    );
  } finally {
    pending.value = false;
  }
}

watch([page, publishedFilter], load, { immediate: true });

const articles = computed(() => data.value?.items || []);
const total = computed(() => data.value?.total || 0);

function setFilter(f: boolean | null) {
  publishedFilter.value = f;
  page.value = 1;
}

async function togglePublish(article: AdminBlogResponse) {
  try {
    await adminService.toggleBlogPublish(article.id);
    useToast().add({
      title: article.published ? "已下架" : "已发布",
      color: "success",
    });
    await load();
  } catch (e: any) {
    useToast().add({ title: e?.message || "操作失败", color: "error" });
  }
}

async function deleteArticle(article: AdminBlogResponse) {
  if (!confirm(`确定删除文章「${article.title}」？`)) return;
  try {
    await adminService.deleteBlog(article.id);
    useToast().add({ title: "文章已删除", color: "success" });
    await load();
  } catch (e: any) {
    useToast().add({ title: e?.message || "删除失败", color: "error" });
  }
}
</script>
