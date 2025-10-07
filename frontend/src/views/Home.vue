<template>
  <div class="ark-home-container">
    <!-- 背景层 -->
    <div class="ark-bg-layer">
      <div class="ark-bg-gradient"></div>
      <!-- 背景图案装饰 -->
      <div class="ark-bg-pattern"></div>
    </div>

    <!-- 顶部导航 -->
    <header class="ark-header">
      <div class="ark-header-content">
        <div class="ark-logo">
          <img
            src="https://ak.hypergryph.com/assets/index/images/ak/pc/logo.png"
            alt="明日方舟"
          />
        </div>
        <nav class="ark-nav">
          <ul>
            <li>
              <router-link to="/" class="nav-link active">首页</router-link>
            </li>
            <li>
              <router-link to="/articles" class="nav-link">文章</router-link>
            </li>
            <li>
              <router-link to="/about" class="nav-link">关于</router-link>
            </li>
            <li>
              <router-link to="/contact" class="nav-link">联系</router-link>
            </li>
          </ul>
        </nav>
        <div class="ark-user-actions">
          <router-link to="/login" class="btn-login">登录</router-link>
          <router-link to="/register" class="btn-register">注册</router-link>
        </div>
      </div>
    </header>

    <!-- 英雄区域 -->
    <section class="ark-hero">
      <div class="ark-hero-content">
        <div class="ark-hero-text">
          <h1 class="ark-hero-title">
            <span class="text-glow">技术博客</span>
          </h1>
          <p class="ark-hero-subtitle">探索科技世界的无限可能</p>
          <div class="ark-hero-buttons">
            <router-link to="/articles" class="btn-primary">
              探索文章
            </router-link>
            <router-link to="/register" class="btn-secondary">
              加入我们
            </router-link>
          </div>
        </div>
        <div class="ark-hero-image">
          <!-- 这里可以放置明日方舟风格的插图 -->
          <div class="ark-character"></div>
        </div>
      </div>
    </section>

    <!-- 内容区域 -->
    <main class="ark-main">
      <!-- 精选内容 -->
      <section class="ark-featured">
        <div class="ark-section-header">
          <h2 class="ark-section-title">
            <span class="title-decoration">//</span>
            最新文章
          </h2>
          <div class="ark-section-divider"></div>
        </div>

        <div class="ark-articles-grid">
          <div
            class="ark-article-card"
            v-for="article in articles"
            :key="article.id"
          >
            <div class="ark-article-card-inner">
              <div class="ark-article-image"></div>
              <div class="ark-article-content">
                <h3 class="ark-article-title">{{ article.title }}</h3>
                <p class="ark-article-excerpt">{{ article.excerpt }}</p>
                <div class="ark-article-meta">
                  <span class="ark-article-author">{{ article.author }}</span>
                  <span class="ark-article-date">{{ article.date }}</span>
                </div>
                <router-link
                  :to="`/article/${article.id}`"
                  class="ark-article-link"
                >
                  阅读更多 <i class="fa fa-angle-right"></i>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <div class="ark-section-footer">
          <router-link to="/articles" class="btn-more">
            查看全部文章 <i class="fa fa-long-arrow-right"></i>
          </router-link>
        </div>
      </section>

      <!-- 特色模块 -->
      <section class="ark-features">
        <div class="ark-section-header">
          <h2 class="ark-section-title">
            <span class="title-decoration">//</span>
            特色内容
          </h2>
          <div class="ark-section-divider"></div>
        </div>

        <div class="ark-features-grid">
          <div class="ark-feature-card">
            <div class="ark-feature-icon">
              <i class="fa fa-code"></i>
            </div>
            <h3 class="ark-feature-title">前沿技术</h3>
            <p class="ark-feature-description">
              探索最新的开发技术和框架，保持技术领先优势
            </p>
          </div>

          <div class="ark-feature-card">
            <div class="ark-feature-icon">
              <i class="fa fa-book"></i>
            </div>
            <h3 class="ark-feature-title">学习资源</h3>
            <p class="ark-feature-description">
              丰富的学习资料和教程，助力你的技术成长
            </p>
          </div>

          <div class="ark-feature-card">
            <div class="ark-feature-icon">
              <i class="fa fa-comments"></i>
            </div>
            <h3 class="ark-feature-title">技术社区</h3>
            <p class="ark-feature-description">
              加入我们的技术社区，与志同道合的开发者交流
            </p>
          </div>
        </div>
      </section>
    </main>

    <!-- 底部区域 -->
    <footer class="ark-footer">
      <div class="ark-footer-content">
        <div class="ark-footer-logo">
          <img
            src="https://ak.hypergryph.com/assets/index/images/ak/pc/logo.png"
            alt="明日方舟"
          />
        </div>
        <div class="ark-footer-links">
          <div class="ark-footer-column">
            <h4>内容</h4>
            <ul>
              <li><router-link to="/articles">文章</router-link></li>
              <li><router-link to="/categories">分类</router-link></li>
              <li><router-link to="/tags">标签</router-link></li>
            </ul>
          </div>
          <div class="ark-footer-column">
            <h4>关于</h4>
            <ul>
              <li><router-link to="/about">关于我们</router-link></li>
              <li><router-link to="/contact">联系我们</router-link></li>
              <li><router-link to="/privacy">隐私政策</router-link></li>
            </ul>
          </div>
        </div>
        <div class="ark-footer-copyright">
          <p>© 2024 明日方舟风格技术博客. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 临时测试数据
const articles = [
  {
    id: 1,
    title: "Vue3最佳实践",
    excerpt: "探索Vue3组合式API的高级用法，提升开发效率和代码质量...",
    author: "ChenXu",
    date: "2024-03-20",
  },
  {
    id: 2,
    title: "TypeScript类型体操",
    excerpt: "深入理解TypeScript类型系统，掌握高级类型技巧...",
    author: "ChenXu",
    date: "2024-03-19",
  },
  {
    id: 3,
    title: "前端性能优化实战",
    excerpt: "分享前端性能优化的实用技巧和最佳实践...",
    author: "ChenXu",
    date: "2024-03-18",
  },
  {
    id: 4,
    title: "微服务架构设计",
    excerpt: "探讨微服务架构的设计原则和实现方法...",
    author: "ChenXu",
    date: "2024-03-17",
  },
];
</script>

<style scoped>
/* 基础样式 */
.ark-home-container {
  min-height: 100vh;
  background-color: #0d0f15;
  color: #e0e0e0;
  position: relative;
  overflow: hidden;
}

/* 背景样式 */
.ark-bg-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.ark-bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0d0f15 0%, #1a1e2a 100%);
}

.ark-bg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiMyMDIwMjAiIGZpbGwtb3BhY2l0eT0iMC4wOCI+PHBhdGggZD0iTTM2IDM0djE0aDE0VjM0aC0xNHptMC0xN2g0djE0aC00di0xNHptLTE0IDBoNHYxNGgtNHYtMTR6bTAgMjBoNHYxNGgtNHYtMTR6bTAgMjBoNHYtMTRoLTQuMDF2LTR6bS0xNCAwSDAgMjBoMTJ2LTRIMHoiLz48L2c+PC9nPjwvc3ZnPg==");
  opacity: 0.2;
}

/* 头部导航样式 */
.ark-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: rgba(13, 15, 21, 0.85);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.ark-header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ark-logo img {
  height: 40px;
  filter: brightness(0) invert(1);
}

.ark-nav ul {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-link {
  color: #e0e0e0;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  position: relative;
  transition: color 0.3s ease;
  padding: 0.5rem 0;
}

.nav-link:hover,
.nav-link.active {
  color: #ff4d4f;
}

.nav-link::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #ff4d4f;
  transition: width 0.3s ease;
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}

.ark-user-actions {
  display: flex;
  gap: 1rem;
}

.btn-login,
.btn-register {
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-login {
  background-color: transparent;
  color: #e0e0e0;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-login:hover {
  border-color: #ff4d4f;
  color: #ff4d4f;
}

.btn-register {
  background-color: #ff4d4f;
  color: white;
  border: 1px solid #ff4d4f;
}

.btn-register:hover {
  background-color: #ff7875;
  border-color: #ff7875;
}

/* 英雄区域样式 */
.ark-hero {
  padding: 12rem 2rem 6rem;
  position: relative;
  overflow: hidden;
}

.ark-hero-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4rem;
}

.ark-hero-text {
  max-width: 600px;
}

.ark-hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
  position: relative;
}

.text-glow {
  color: #fff;
  text-shadow:
    0 0 10px rgba(255, 77, 79, 0.5),
    0 0 20px rgba(255, 77, 79, 0.3);
}

.ark-hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  color: #b0b0b0;
}

.ark-hero-buttons {
  display: flex;
  gap: 1.5rem;
}

.btn-primary,
.btn-secondary {
  padding: 1rem 2.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 77, 79, 0.5);
}

.btn-secondary {
  background-color: transparent;
  color: #e0e0e0;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: #ff4d4f;
  color: #ff4d4f;
}

.ark-hero-image {
  flex: 1;
  position: relative;
  min-height: 400px;
}

.ark-character {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background-image: url("https://ak.hypergryph.com/assets/index/images/ak/pc/IndexSplash.png");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: right center;
  filter: drop-shadow(0 0 15px rgba(255, 77, 79, 0.3));
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 主要内容样式 */
.ark-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 4rem;
  position: relative;
}

/* 通用区域样式 */
.ark-section-header {
  margin-bottom: 3rem;
  text-align: center;
}

.ark-section-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #fff;
  position: relative;
  display: inline-block;
}

.title-decoration {
  color: #ff4d4f;
  margin-right: 0.5rem;
}

.ark-section-divider {
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, #ff4d4f, #ff7875);
  margin: 0 auto;
  border-radius: 2px;
}

/* 精选文章样式 */
.ark-articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.ark-article-card {
  background-color: rgba(26, 30, 42, 0.7);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
}

.ark-article-card:hover {
  transform: translateY(-5px);
  border-color: #ff4d4f;
  box-shadow: 0 10px 20px rgba(255, 77, 79, 0.2);
}

.ark-article-card-inner {
  position: relative;
}

.ark-article-image {
  height: 180px;
  background: linear-gradient(135deg, #1a1e2a 0%, #2c3142 100%);
  position: relative;
  overflow: hidden;
}

.ark-article-image::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXR0ZXJuIGlkPSJncmlkIiB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiPjxwYXRoIGQ9Ik0gNDAgMCBMIDAgMCAwIDQwIiBmaWxsPSJub25lIiBzdHJva2U9IiNmZjRkNGYiIHN0cm9rZS13aWR0aD0iMSIgb3BhY2l0eT0iMC4xIi8+PC9wYXR0ZXJuPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiIC8+PC9zdmc+");
  opacity: 0.3;
}

.ark-article-content {
  padding: 1.5rem;
}

.ark-article-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #fff;
  transition: color 0.3s ease;
}

.ark-article-card:hover .ark-article-title {
  color: #ff4d4f;
}

.ark-article-excerpt {
  color: #b0b0b0;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.ark-article-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  color: #888;
  font-size: 0.9rem;
}

.ark-article-link {
  display: inline-flex;
  align-items: center;
  color: #ff4d4f;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.ark-article-link:hover {
  transform: translateX(5px);
}

.ark-article-link i {
  margin-left: 0.5rem;
  transition: transform 0.3s ease;
}

.ark-article-link:hover i {
  transform: translateX(3px);
}

.ark-section-footer {
  text-align: center;
}

.btn-more {
  display: inline-flex;
  align-items: center;
  padding: 0.8rem 2rem;
  background-color: transparent;
  color: #e0e0e0;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-more:hover {
  border-color: #ff4d4f;
  color: #ff4d4f;
  background-color: rgba(255, 77, 79, 0.1);
}

.btn-more i {
  margin-left: 0.5rem;
  transition: transform 0.3s ease;
}

.btn-more:hover i {
  transform: translateX(3px);
}

/* 特色模块样式 */
.ark-features {
  margin-top: 6rem;
  position: relative;
}

.ark-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.ark-feature-card {
  background-color: rgba(26, 30, 42, 0.7);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
}

.ark-feature-card:hover {
  transform: translateY(-5px);
  border-color: #ff4d4f;
  box-shadow: 0 10px 20px rgba(255, 77, 79, 0.2);
}

.ark-feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  box-shadow: 0 6px 12px rgba(255, 77, 79, 0.4);
}

.ark-feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #fff;
}

.ark-feature-description {
  color: #b0b0b0;
  line-height: 1.6;
}

/* 底部样式 */
.ark-footer {
  background-color: rgba(13, 15, 21, 0.9);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 4rem 2rem;
  position: relative;
  backdrop-filter: blur(10px);
}

.ark-footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.ark-footer-logo img {
  height: 40px;
  filter: brightness(0) invert(1);
  margin-bottom: 1rem;
}

.ark-footer-links {
  display: flex;
  gap: 4rem;
  margin-bottom: 2rem;
}

.ark-footer-column h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 1rem;
}

.ark-footer-column ul {
  list-style: none;
}

.ark-footer-column ul li {
  margin-bottom: 0.5rem;
}

.ark-footer-column ul li a {
  color: #b0b0b0;
  text-decoration: none;
  transition: color 0.3s ease;
}

.ark-footer-column ul li a:hover {
  color: #ff4d4f;
}

.ark-footer-copyright {
  color: #888;
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .ark-hero-content {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }

  .ark-hero-image {
    width: 80%;
  }
}

@media (max-width: 992px) {
  .ark-header-content {
    flex-direction: column;
    gap: 1.5rem;
    padding: 1rem;
  }

  .ark-nav ul {
    gap: 1.5rem;
  }

  .ark-hero-title {
    font-size: 3rem;
  }
}

@media (max-width: 768px) {
  .ark-hero {
    padding: 10rem 1rem 4rem;
  }

  .ark-hero-title {
    font-size: 2.5rem;
  }

  .ark-hero-subtitle {
    font-size: 1.2rem;
  }

  .ark-hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .ark-articles-grid,
  .ark-features-grid {
    grid-template-columns: 1fr;
  }

  .ark-footer-links {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 2rem;
  }
}

@media (max-width: 576px) {
  .ark-hero-title {
    font-size: 2rem;
  }

  .ark-hero-subtitle {
    font-size: 1rem;
  }

  .btn-primary,
  .btn-secondary {
    padding: 0.8rem 2rem;
    font-size: 1rem;
  }
}
</style>
