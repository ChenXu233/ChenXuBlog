<template>
  <div class="min-h-screen bg-slate-100 dark:bg-slate-900">
    <div class="flex">
      <!-- Sidebar -->
      <aside
        class="w-56 shrink-0 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 min-h-screen"
      >
        <div class="p-4">
          <h1 class="text-lg font-bold mb-6">管理后台</h1>
          <nav class="space-y-1">
            <NuxtLink
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
              :class="{
                'bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400':
                  route.path === item.to,
              }"
            >
              <UIcon :name="item.icon" class="w-4 h-4" />
              {{ item.label }}
            </NuxtLink>
          </nav>
        </div>
        <div class="p-4 border-t border-slate-200 dark:border-slate-700">
          <NuxtLink
            to="/home"
            class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-800 dark:hover:text-gray-200"
          >
            <UIcon name="i-heroicons-arrow-left" class="w-4 h-4" />
            返回首页
          </NuxtLink>
        </div>
      </aside>

      <!-- Content -->
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const navItems = [
  { to: "/admin", label: "仪表盘", icon: "i-heroicons-squares-2x2" },
  { to: "/admin/users", label: "用户管理", icon: "i-heroicons-users" },
  { to: "/admin/roles", label: "角色管理", icon: "i-heroicons-shield-check" },
  {
    to: "/admin/articles",
    label: "文章管理",
    icon: "i-heroicons-document-text",
  },
  {
    to: "/admin/comments",
    label: "评论管理",
    icon: "i-heroicons-chat-bubble-left-right",
  },
];
</script>
