<template>
  <nav class="main-nav">
    <div class="nav-brand">ChenXu博客</div>
    <div class="nav-links">
      <template v-if="!authStore.isAuthenticated">
        <router-link to="/login" class="nav-link">登录</router-link>
        <router-link to="/register" class="nav-link">注册</router-link>
      </template>
      <template v-else>
        <span class="user-info">{{ authStore.user.username }}</span>
        <button @click="authStore.logout" class="logout-btn">退出</button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";
const authStore = useAuthStore();
</script>

<style scoped>
.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50;
  color: white;
  padding: 0 24px;
  height: 64px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-brand {
  font-size: 24px;
  font-weight: bold;
  color: #ecf0f1;
  text-decoration: none;
  letter-spacing: 1px;
  transition: color 0.3s ease;
}

.nav-brand:hover {
  color: #3498db;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 16px;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #3498db;
}

.user-info {
  color: #ecf0f1;
  font-size: 16px;
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #c0392b;
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-nav {
    padding: 0 16px;
  }

  .nav-brand {
    font-size: 20px;
  }

  .nav-links {
    gap: 12px;
  }

  .nav-link,
  .logout-btn {
    padding: 6px 12px;
    font-size: 14px;
  }
}
</style>
