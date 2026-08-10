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
        <template #published-data="{ row }">
          <UBadge :color="row.published ? 'success' : 'warning'" variant="soft">
            {{ row.published ? "已发布" : "草稿" }}
          </UBadge>
        </template>
        <template #view_count-data="{ row }">
          <span class="text-sm text-gray-500">{{ row.view_count }}</span>
        </template>
        <template #actions-data="{ row }">
          <div class="flex gap-1">
            <UButton
              icon="i-heroicons-eye"
              size="xs"
              variant="ghost"
              :to="`/article/${row.id}`"
            />
            <UButton
              icon="i-heroicons-paper-airplane"
              size="xs"
              variant="ghost"
              :color="row.published ? 'warning' : 'success'"
              @click="togglePublish(row)"
            />
            <UButton
              icon="i-heroicons-trash"
              size="xs"
              variant="ghost"
              color="error"
              @click="deleteArticle(row)"
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

interface AdminBlog {
  id: number;
  title: string;
  username: string;
  published: boolean;
  view_count: number;
}

const auth = useAuthStore();
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

const { data, pending, refresh } = useAuthFetch<{
  items: AdminBlog[];
  total: number;
}>(
  () => {
    const pub =
      publishedFilter.value === null
        ? ""
        : `&published=${publishedFilter.value}`;
    return `/apis/v1/admin/blogs?page=${page.value}&page_size=${pageSize}${pub}`;
  },
  { watch: [page, publishedFilter] },
);

const articles = computed(() => data.value?.items || []);
const total = computed(() => data.value?.total || 0);

function setFilter(f: boolean | null) {
  publishedFilter.value = f;
  page.value = 1;
}

async function togglePublish(article: AdminBlog) {
  try {
    await $fetch(`/apis/v1/admin/blogs/${article.id}/publish`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    useToast().add({
      title: article.published ? "已下架" : "已发布",
      color: "success",
    });
    refresh();
  } catch (e: any) {
    useToast().add({ title: e?.data?.detail || "操作失败", color: "error" });
  }
}

async function deleteArticle(article: AdminBlog) {
  if (!confirm(`确定删除文章「${article.title}」？`)) return;
  try {
    await $fetch(`/apis/v1/admin/blogs/${article.id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    useToast().add({ title: "文章已删除", color: "success" });
    refresh();
  } catch (e: any) {
    useToast().add({ title: e?.data?.detail || "删除失败", color: "error" });
  }
}
</script>
