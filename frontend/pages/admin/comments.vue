<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">评论管理</h2>

    <UCard>
      <UTable :data="comments" :columns="columns" :loading="pending">
        <template #content-data="{ row }">
          <span class="line-clamp-1 text-sm">{{ row.content }}</span>
        </template>
        <template #actions-data="{ row }">
          <UButton
            icon="i-heroicons-trash"
            size="xs"
            variant="ghost"
            color="error"
            @click="deleteComment(row)"
          />
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

interface AdminComment {
  id: number;
  blog_id: number;
  blog_title: string;
  username: string;
  content: string;
}

const auth = useAuthStore();
const page = ref(1);
const pageSize = 10;

const columns = [
  { accessorKey: "id", header: "ID" },
  { accessorKey: "username", header: "用户" },
  { accessorKey: "blog_title", header: "文章" },
  { accessorKey: "content", header: "内容" },
  { accessorKey: "actions", header: "操作" },
];

const { data, pending, refresh } = useAuthFetch<{
  items: AdminComment[];
  total: number;
}>(() => `/apis/v1/admin/comments?page=${page.value}&page_size=${pageSize}`, {
  watch: [page],
});

const comments = computed(() => data.value?.items || []);
const total = computed(() => data.value?.total || 0);

async function deleteComment(comment: AdminComment) {
  if (!confirm("确定删除该评论？")) return;
  try {
    await $fetch(`/apis/v1/admin/comments/${comment.id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    useToast().add({ title: "评论已删除", color: "success" });
    refresh();
  } catch (e: any) {
    useToast().add({ title: e?.data?.detail || "删除失败", color: "error" });
  }
}
</script>
