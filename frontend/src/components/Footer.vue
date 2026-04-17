<template>
  <footer class="main-footer">
    <div class="footer-content">
      <div class="footer-info">
        <div class="footer-logo">ChenXu博客</div>
        <p class="footer-description">分享知识，记录生活</p>
      </div>
      <div class="footer-links">
        <router-link to="/" class="footer-link">首页</router-link>
        <router-link to="/about" class="footer-link">关于我</router-link>
        <router-link to="/archive" class="footer-link">文章归档</router-link>
        <router-link to="/contact" class="footer-link">联系我</router-link>
      </div>
    </div>
    <div class="footer-copyright">
      <p>© 2024 ChenXu博客 保留所有权利</p>
      <p class="icp-info">
        <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener"
          >浙ICP备2026024319号-1</a
        >
      </p>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.main-footer {
  background: var(--color-bg-secondary);
  border-top: 1px solid var(--color-border);
  color: var(--color-text-light);
  padding: 40px 24px 20px;
  margin-top: auto;
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
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 8px;
}

.footer-description {
  font-size: 14px;
  color: var(--color-text-light);
}

.footer-links {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.footer-link {
  color: var(--color-text-light);
  text-decoration: none;
  font-size: 14px;
  padding: 8px 12px;
  border-radius: var(--radius);
  transition: all var(--transition);
}

.footer-link:hover {
  color: var(--color-primary);
  background: var(--color-bg);
}

.footer-copyright {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  font-size: 13px;
}

.icp-info {
  margin-top: 8px;
  margin-bottom: 8vh;
}

.icp-info a {
  color: var(--color-text-light);
  text-decoration: none;
}

.icp-info a:hover {
  color: var(--color-primary);
}

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
  }
}
</style>
