<template>
  <nav class="main-nav">
    <div class="nav-brand">
      <router-link to="/" class="brand-text">ChenXu博客</router-link>
    </div>
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
import { useUserStore } from "../stores/userStore";
const authStore = useUserStore();
</script>

<style scoped>
.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  padding: 0 24px;
  height: 64px;
  box-shadow: var(--shadow);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  transition: var(--transition);
}

.nav-brand {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-text);
  text-decoration: none;
  letter-spacing: 0.5px;
}

.brand-text {
  color: var(--color-text);
  text-decoration: none;
  transition: color var(--transition);
}

.brand-text:hover {
  color: var(--color-primary);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-link {
  color: var(--color-text-light);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: var(--radius);
  transition: all var(--transition);
}

.nav-link:hover {
  color: var(--color-primary);
  background: var(--color-bg-secondary);
}

.nav-link.router-link-active {
  color: var(--color-primary);
}

.user-info {
  color: var(--color-text-light);
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
}

.logout-btn {
  background: var(--color-primary);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: var(--radius);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);
}

.logout-btn:hover {
  background: var(--color-primary-hover);
}

@media (max-width: 768px) {
  .main-nav {
    padding: 0 16px;
    height: 56px;
  }

  .nav-brand {
    font-size: 18px;
  }

  .nav-link,
  .user-info,
  .logout-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>
