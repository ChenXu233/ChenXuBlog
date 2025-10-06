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
  background: transparent;
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  color: white;
  padding: 0 24px;
  height: 64px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  transition: all 0.3s ease;
  transform-style: preserve-3d;
}

/* 滚动时的效果 - 使用更活泼的颜色 */
.main-nav.scrolled {
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #ff9a8b, #ff6a88);
  transform: translateY(-2px);
}

.nav-brand {
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  text-decoration: none;
  letter-spacing: 1.2px;
  cursor: pointer;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.brand-text {
  position: relative;
  display: inline-block;
  transition: all 0.3s ease;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand-text::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 3px;
  background: linear-gradient(90deg, #ffecd2, #fcb69f);
  transition: width 0.3s ease;
  border-radius: 3px;
}

.nav-brand:hover .brand-text {
  color: #fcb69f;
  transform: translateY(-3px) scale(1.05);
}

.nav-brand:hover .brand-text::after {
  width: 100%;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 25px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  z-index: 1;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-link::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: all 0.5s ease;
  z-index: -1;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.25);
  color: #fff;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.nav-link:hover::before {
  left: 100%;
}

.user-info {
  color: #fff;
  font-size: 16px;
  font-weight: 500;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
}

.logout-btn {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  z-index: 1;
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
}

.logout-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: all 0.4s ease;
  z-index: -1;
}

.logout-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(245, 87, 108, 0.45);
  background: linear-gradient(135deg, #f5576c, #f093fb);
}

.logout-btn:hover::before {
  left: 100%;
}

.logout-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
}

/* 响应式设计 - 增强移动端体验 */
@media (max-width: 768px) {
  .main-nav {
    padding: 0 16px;
    height: 56px;
  }

  .nav-brand {
    font-size: 22px;
  }

  .nav-links {
    gap: 12px;
  }

  .nav-link,
  .user-info,
  .logout-btn {
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 20px;
  }
}

/* 添加一些微动画效果，提升活泼感 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.03);
  }
  100% {
    transform: scale(1);
  }
}

/* 可以在特殊事件或状态下使用这个动画 */
.main-nav.animated {
  animation: pulse 2s infinite;
}
</style>
