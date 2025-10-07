<template>
  <footer class="main-footer">
    <div class="footer-content">
      <div class="footer-info">
        <div class="footer-logo">ChenXu博客</div>
        <p class="footer-description">分享知识，记录生活</p>
      </div>
      <div class="footer-links">
        <router-link
          to="/"
          class="footer-link"
          @mouseenter="hoveredLink = 'home'"
          @mouseleave="hoveredLink = ''"
          >首页</router-link
        >
        <router-link
          to="/about"
          class="footer-link"
          @mouseenter="hoveredLink = 'about'"
          @mouseleave="hoveredLink = ''"
          >关于我</router-link
        >
        <router-link
          to="/archive"
          class="footer-link"
          @mouseenter="hoveredLink = 'archive'"
          @mouseleave="hoveredLink = ''"
          >文章归档</router-link
        >
        <router-link
          to="/contact"
          class="footer-link"
          @mouseenter="hoveredLink = 'contact'"
          @mouseleave="hoveredLink = ''"
          >联系我</router-link
        >
      </div>
    </div>
    <div class="footer-copyright">
      <p>© 2024 ChenXu博客 保留所有权利</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

// 用于处理悬停效果的响应式数据
const hoveredLink = ref("");
</script>

<style scoped>
.main-footer {
  background: linear-gradient(
    135deg,
    rgba(125, 173, 252, 0.6),
    rgba(245, 87, 108, 0.6)
  );
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  color: white;
  padding: 40px 24px 20px;
  margin-top: auto;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto 30px;
  flex-wrap: wrap;
  gap: 30px;
}

.footer-info {
  flex: 1;
  min-width: 200px;
}

.footer-logo {
  font-size: 26px;
  font-weight: 700;
  color: white;
  margin-bottom: 10px;
  letter-spacing: 1.2px;
  transition: all 0.3s ease;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  display: inline-block;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.footer-logo::after {
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

.footer-logo:hover {
  color: #fcb69f;
  transform: translateY(-3px) scale(1.05);
}

.footer-logo:hover::after {
  width: 100%;
}

.footer-description {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  line-height: 1.5;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.footer-links {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.footer-link {
  color: white;
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

.footer-link::before {
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

.footer-link:hover {
  background-color: rgba(255, 255, 255, 0.25);
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.footer-link:hover::before {
  left: 100%;
}

.footer-copyright {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-footer {
    padding: 30px 16px 15px;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
    gap: 20px;
    margin-bottom: 20px;
  }

  .footer-links {
    justify-content: center;
    gap: 16px;
  }

  .footer-logo {
    font-size: 22px;
  }

  .footer-link {
    font-size: 14px;
    padding: 8px 16px;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.main-footer {
  animation:
    fadeIn 0.5s ease-out,
    gradientShift 15s ease infinite;
  background-size: 400% 400%;
}
</style>
