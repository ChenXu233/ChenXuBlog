<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="admin-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo" v-if="!sidebarCollapsed">
          <span class="logo-icon">⚙️</span>
          <span class="logo-text">管理后台</span>
        </div>
        <button
          class="collapse-btn"
          @click="sidebarCollapsed = !sidebarCollapsed"
        >
          {{ sidebarCollapsed ? "→" : "←" }}
        </button>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-text" v-if="!sidebarCollapsed">{{
            item.label
          }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info" v-if="!sidebarCollapsed">
          <el-avatar
            :size="32"
            src="https://avatars.githubusercontent.com/u/91937041?v=4"
          />
          <div class="user-detail">
            <span class="username">{{ username }}</span>
            <span class="role">管理员</span>
          </div>
        </div>
        <router-link to="/home" class="back-home">
          {{ sidebarCollapsed ? "🏠" : "返回首页" }}
        </router-link>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="admin-main">
      <header class="main-header">
        <h1 class="page-title">{{ currentTitle }}</h1>
        <div class="header-actions">
          <span class="current-time">{{ currentTime }}</span>
        </div>
      </header>

      <div class="main-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../../stores/authStore";

const route = useRoute();
const authStore = useAuthStore();

const sidebarCollapsed = ref(false);
const currentTime = ref("");

const username = computed(() => authStore.user?.username || "Admin");

const navItems = [
  { path: "/admin", label: "仪表盘", icon: "📊", name: "dashboard" },
  { path: "/admin/users", label: "用户管理", icon: "👥", name: "user-manage" },
  { path: "/admin/roles", label: "角色管理", icon: "🔐", name: "role-manage" },
  {
    path: "/admin/articles",
    label: "文章管理",
    icon: "📝",
    name: "article-manage",
  },
  {
    path: "/admin/comments",
    label: "评论管理",
    icon: "💬",
    name: "comment-manage",
  },
];

const currentTitle = computed(() => {
  const item = navItems.find((i) => i.path === route.path);
  return item?.label || "管理后台";
});

const isActive = (path: string) => {
  if (path === "/admin") return route.path === "/admin";
  return route.path.startsWith(path);
};

const updateTime = () => {
  currentTime.value = new Date().toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

let timer = 0;

onMounted(() => {
  updateTime();
  timer = window.setInterval(updateTime, 1000);
});

onUnmounted(() => {
  clearInterval(timer);
});
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

/* 侧边栏 */
.admin-sidebar {
  width: 240px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background: rgba(26, 26, 46, 0.85);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  z-index: 100;
}

.admin-sidebar.collapsed {
  width: 72px;
}

.sidebar-header {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  font-family: "PingFang SC", sans-serif;
}

.collapse-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 导航 */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s ease;
  font-family: "PingFang SC", sans-serif;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.nav-item.active {
  background: rgba(244, 179, 194, 0.15);
  color: #f4b3c2;
  border: 1px solid rgba(244, 179, 194, 0.3);
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.admin-sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px;
}

/* 底部 */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-detail {
  display: flex;
  flex-direction: column;
}

.username {
  color: #fff;
  font-size: 14px;
  font-weight: 500;
}

.role {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
}

.back-home {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 13px;
  transition: all 0.2s;
}

.back-home:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* 主内容区 */
.admin-main {
  flex: 1;
  margin-left: 240px;
  min-height: 100vh;
  transition: margin-left 0.3s ease;
}

.admin-sidebar.collapsed + .admin-main {
  margin-left: 72px;
}

.main-header {
  position: sticky;
  top: 0;
  padding: 20px 32px;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 50;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  font-family: "PingFang SC", sans-serif;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.current-time {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  font-family: "JetBrains Mono", monospace;
}

.main-content {
  padding: 24px 32px;
}
</style>
