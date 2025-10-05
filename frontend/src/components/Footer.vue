<template>
  <footer class="main-footer">
    <div class="footer-content">
      <div class="footer-info">
        <div class="footer-logo">ChenXu博客</div>
        <p class="footer-description">分享知识，记录生活</p>
      </div>
      <div class="footer-links">
        <a
          href="/"
          class="footer-link"
          @mouseenter="hoveredLink = 'home'"
          @mouseleave="hoveredLink = ''"
          >首页</a
        >
        <a
          href="/about"
          class="footer-link"
          @mouseenter="hoveredLink = 'about'"
          @mouseleave="hoveredLink = ''"
          >关于我</a
        >
        <a
          href="/archive"
          class="footer-link"
          @mouseenter="hoveredLink = 'archive'"
          @mouseleave="hoveredLink = ''"
          >文章归档</a
        >
        <a
          href="/contact"
          class="footer-link"
          @mouseenter="hoveredLink = 'contact'"
          @mouseleave="hoveredLink = ''"
          >联系我</a
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

// 用于处理悬停效果的响应式数据
const hoveredLink = ref("");
</script>

<style scoped>
.main-footer {
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 40px 24px 20px;
  margin-top: auto;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
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
  font-size: 24px;
  font-weight: bold;
  color: #ecf0f1;
  margin-bottom: 10px;
  letter-spacing: 1px;
  transition: color 0.3s ease;
}

.footer-logo:hover {
  color: #3498db;
}

.footer-description {
  color: #bdc3c7;
  font-size: 14px;
  line-height: 1.5;
}

.footer-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.footer-link {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 16px;
  padding: 8px 0;
  position: relative;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #3498db;
}

.footer-link::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #3498db;
  transition: width 0.3s ease;
}

.footer-link:hover::after {
  width: 100%;
}

.footer-copyright {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #95a5a6;
  font-size: 14px;
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
    font-size: 20px;
  }

  .footer-link {
    font-size: 14px;
  }
}

/* 添加一些微动画效果 */
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

.main-footer {
  animation: fadeIn 0.5s ease-out;
}
</style>
