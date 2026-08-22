<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">评论管理</h2>

    <UCard>
      <UTable :data="comments" :columns="columns" :loading="pending">
        <template #content-cell="{ row }">
          <span class="line-clamp-1 text-sm">{{ row.original.content }}</span>
        </template>
        <template #actions-cell="{ row }">
          <UButton
            icon="i-heroicons-trash"
            size="xs"
            variant="ghost"
            color="error"
            @click="deleteComment(row.original)"
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

import { adminService } from "~/service/admin";
import type { AdminCommentResponse } from "~/src/client/types.gen";

const page = ref(1);
const pageSize = 10;

const columns = [
  { accessorKey: "id", header: "ID" },
  { accessorKey: "username", header: "用户" },
  { accessorKey: "blog_title", header: "文章" },
  { accessorKey: "content", header: "内容" },
  { accessorKey: "actions", header: "操作" },
];

const data = ref<Awaited<ReturnType<typeof adminService.getComments>> | null>(
  null,
);
const pending = ref(false);

async function load() {
  pending.value = true;
  try {
    data.value = await adminService.getComments(page.value, pageSize);
  } finally {
    pending.value = false;
  }
}

watch([page], load, { immediate: true });

const comments = computed(() => data.value?.items || []);
const total = computed(() => data.value?.total || 0);

async function deleteComment(comment: AdminCommentResponse) {
  if (!confirm("确定删除该评论？")) return;
  try {
    await adminService.deleteComment(comment.id);
    useToast().add({ title: "评论已删除", color: "success" });
    await load();
  } catch (e: any) {
    useToast().add({ title: e?.message || "删除失败", color: "error" });
  }
}
</script>
