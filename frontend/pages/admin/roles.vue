<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">角色管理</h2>

    <div class="grid gap-4 md:grid-cols-2">
      <UCard v-for="role in roles" :key="role.id">
        <template #header>
          <div class="flex justify-between items-center">
            <span class="font-semibold">{{ role.name }}</span>
            <UBadge v-if="role.is_default" variant="soft">默认角色</UBadge>
          </div>
        </template>
        <p v-if="role.description" class="text-sm text-gray-500 mb-3">
          {{ role.description }}
        </p>
        <div class="flex gap-1 flex-wrap">
          <UBadge
            v-for="perm in role.permissions"
            :key="perm"
            variant="soft"
            size="sm"
            color="info"
          >
            {{ perm }}
          </UBadge>
          <span v-if="!role.permissions?.length" class="text-sm text-gray-400"
            >无权限</span
          >
        </div>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth", ssr: false });

import { adminService } from "~/service/admin";

const data = ref<Awaited<ReturnType<typeof adminService.getRoles>> | null>(
  null,
);
const roles = computed(() => data.value || []);

async function load() {
  if (!useAuthStore().token) return;
  data.value = await adminService.getRoles();
}

watch(() => useAuthStore().token, load, { immediate: true });
</script>
