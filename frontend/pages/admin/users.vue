<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">用户管理</h2>

    <UCard>
      <UTable :data="users" :columns="columns" :loading="pending">
        <template #roles-data="{ row }">
          <div class="flex gap-1 flex-wrap">
            <UBadge
              v-for="role in row.roles"
              :key="role"
              variant="soft"
              :color="role === 'superuser' ? 'rose' : 'emerald'"
            >
              {{ role }}
            </UBadge>
          </div>
        </template>
        <template #is_verified-data="{ row }">
          <UBadge
            :color="row.is_verified ? 'success' : 'warning'"
            variant="soft"
          >
            {{ row.is_verified ? "已验证" : "未验证" }}
          </UBadge>
        </template>
        <template #actions-data="{ row }">
          <UButton
            icon="i-heroicons-trash"
            size="xs"
            color="error"
            variant="ghost"
            :disabled="row.id === currentUserId"
            @click="deleteUser(row)"
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

interface AdminUser {
  id: number;
  uuid: string;
  username: string;
  email: string;
  is_verified: boolean;
  roles: string[];
}

const auth = useAuthStore();
const currentUserId = auth.user?.id;
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

const { data, pending, refresh } = useAuthFetch<{
  items: AdminUser[];
  total: number;
}>(() => `/apis/v1/admin/users?page=${page.value}&page_size=${pageSize}`, {
  watch: [page],
});

const users = computed(() => data.value?.items || []);
const total = computed(() => data.value?.total || 0);

async function deleteUser(user: AdminUser) {
  if (!confirm(`确定删除用户 ${user.username}？`)) return;
  try {
    await $fetch(`/apis/v1/admin/users/${user.id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    useToast().add({ title: "用户已删除", color: "success" });
    refresh();
  } catch (e: any) {
    useToast().add({ title: e?.data?.detail || "删除失败", color: "error" });
  }
}
</script>
