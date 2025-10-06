<template>
  <div class="home-container">
    <!-- 主体内容 -->
    <main>
      <!-- 欢迎区域 -->
      <section class="hero">
        <h1>欢迎来到技术博客</h1>
        <p>探索最新技术文章与开发实践</p>
        <div class="cta-buttons">
          <router-link to="/articles" class="cta-button">浏览博客</router-link>
          <router-link to="/register" class="cta-button secondary"
            >立即注册</router-link
          >
          <router-link to="/login" class="cta-button secondary"
            >登录</router-link
          >
        </div>
      </section>

      <!-- 精选文章 -->
      <section class="featured-articles">
        <h2>最新文章</h2>
        <div class="article-grid">
          <div
            class="article-card"
            v-for="article in articles"
            :key="article.id"
          >
            <h3>{{ article.title }}</h3>
            <p class="excerpt">{{ article.excerpt }}</p>
            <div class="article-meta">
              <span class="author">{{ article.author }}</span>
              <span class="date">{{ article.date }}</span>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
// 临时测试数据
const articles = [
  {
    id: 1,
    title: "Vue3最佳实践",
    excerpt: "探索Vue3组合式API的高级用法...",
    author: "ChenXu",
    date: "2024-03-20",
  },
  {
    id: 2,
    title: "TypeScript类型体操",
    excerpt: "深入理解TypeScript类型系统...",
    author: "ChenXu",
    date: "2024-03-19",
  },
];
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: #f8fafc;
}

.navbar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2563eb;
}

.hero {
  text-align: center;
  padding: 4rem 1rem;
  background: linear-gradient(45deg, #2563eb, #1d4ed8);
  color: white;
}

.cta-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.article-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.article-card:hover {
  transform: translateY(-2px);
}

/* 其他样式细节... */
</style>
