<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">用户管理</h2>

    <UCard>
      <UTable :data="users" :columns="columns" :loading="pending">
        <template #roles-cell="{ row }">
          <div class="flex gap-1 flex-wrap">
            <UBadge
              v-for="role in row.original.roles"
              :key="role"
              variant="soft"
              :color="role === 'superuser' ? 'error' : 'success'"
            >
              {{ role }}
            </UBadge>
          </div>
        </template>
        <template #is_verified-cell="{ row }">
          <UBadge
            :color="row.original.is_verified ? 'success' : 'warning'"
            variant="soft"
          >
            {{ row.original.is_verified ? "已验证" : "未验证" }}
          </UBadge>
        </template>
        <template #actions-cell="{ row }">
          <UButton
            icon="i-heroicons-trash"
            size="xs"
            color="error"
            variant="ghost"
            :disabled="row.original.id === currentUserId"
            @click="deleteUser(row.original)"
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
import type { AdminUserResponse } from "~/shared/api-client/types.gen";

const currentUserId = useAuthStore().user?.id;
const page = ref(1);
const pageSize = 10;

const columns = [
  { accessorKey: "id", header: "ID" },
  { accessorKey: "username", header: "用户名" },
  { accessorKey: "email", header: "邮箱" },
  { accessorKey: "roles", header: "角色" },
  { accessorKey: "is_verified", header: "状态" },
  { accessorKey: "actions", header: "操作" },
];

const data = ref<Awaited<ReturnType<typeof adminService.getUsers>> | null>(
  null,
);
const pending = ref(false);

async function load() {
  pending.value = true;
  try {
    data.value = await adminService.getUsers(page.value, pageSize);
  } finally {
    pending.value = false;
  }
}

watch([page], load, { immediate: true });

const users = computed(() => data.value?.items || []);
const total = computed(() => data.value?.total || 0);

async function deleteUser(user: AdminUserResponse) {
  if (!confirm(`确定删除用户 ${user.username}？`)) return;
  try {
    await adminService.deleteUser(user.id);
    useToast().add({ title: "用户已删除", color: "success" });
    await load();
  } catch (e: any) {
    useToast().add({ title: e?.message || "删除失败", color: "error" });
  }
}
</script>
