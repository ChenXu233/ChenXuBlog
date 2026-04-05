<template>
  <div class="article-detail">
    <div v-if="loading" class="loading">
      <i class="fa fa-spinner fa-spin"></i> 加载中...
    </div>
    <article v-else-if="article" class="article-container">
      <header class="article-header">
        <div class="tags" v-if="article.tags_name?.length">
          <span v-for="tag in article.tags_name" :key="tag" class="tag">{{ tag }}</span>
        </div>
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <span class="meta-item">
            <i class="fa fa-calendar"></i>
            {{ formatDate(article.created_at) }}
          </span>
          <span class="meta-item">
            <i class="fa fa-eye"></i>
            {{ article.view_count }} 阅读
          </span>
          <span class="meta-item">
            <i class="fa fa-heart"></i>
            {{ article.like }} 点赞
          </span>
        </div>
      </header>

      <div class="article-cover" v-if="article.cover_url">
        <img :src="article.cover_url" :alt="article.title" />
      </div>

      <div class="article-body" v-html="renderedContent"></div>

      <footer class="article-footer">
        <div class="actions">
          <button @click="handleLike" class="action-btn" :class="{ active: hasLiked }">
            <i class="fa fa-thumbs-up"></i> 点赞 {{ article.like }}
          </button>
          <button v-if="canEdit" @click="goToEdit" class="action-btn">
            <i class="fa fa-edit"></i> 编辑
          </button>
        </div>
      </footer>

      <CommentList ref="commentListRef" :blogId="article.id" />
    </article>
    <div v-else class="not-found">
      <h2>文章不存在</h2>
      <router-link to="/home">返回首页</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import MarkdownIt from "markdown-it";
import { blogService } from "../service/blog";
import { useTokenStore } from "../stores/token";
import { useUserStore } from "../stores/userStore";
import CommentList from "../components/CommentList.vue";
import { showError } from "../utils/request";
import type { Article } from "../types/article";

const route = useRoute();
const router = useRouter();
const tokenStore = useTokenStore();
const userStore = useUserStore();

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

const article = ref<Article | null>(null);
const loading = ref(true);
const hasLiked = ref(false);
const commentListRef = ref<InstanceType<typeof CommentList> | null>(null);

const renderedContent = computed(() => {
  return article.value ? md.render(article.value.body) : "";
});

const canEdit = computed(() => {
  return (
    tokenStore.isAuthenticated &&
    userStore.id &&
    article.value?.user_uuid === userStore.id
  );
});

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const fetchArticle = async () => {
  loading.value = true;
  const id = Number(route.params.id);
  try {
    article.value = await blogService.getBlog(id);
  } catch (error) {
    showError("加载文章失败");
  } finally {
    loading.value = false;
  }
};

const handleLike = () => {
  hasLiked.value = !hasLiked.value;
  if (article.value) {
    article.value.like += hasLiked.value ? 1 : -1;
  }
};

const goToEdit = () => {
  router.push(`/article/edit/${article.value?.id}`);
};

onMounted(() => {
  fetchArticle();
});
</script>

<style scoped>
.article-detail {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.loading,
.not-found {
  text-align: center;
  padding: 64px 24px;
  color: var(--color-text-light, #666);
}

.loading i {
  font-size: 24px;
}

.article-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.article-header {
  margin-bottom: 24px;
}

.tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 12px;
  border-radius: 20px;
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  line-height: 1.3;
  margin-bottom: 16px;
}

.article-meta {
  display: flex;
  gap: 24px;
  color: #999;
  font-size: 14px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.article-cover {
  margin-bottom: 24px;
  border-radius: 12px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
}

.article-body {
  line-height: 1.8;
  font-size: 16px;
  color: #333;
}

.article-body :deep(h1),
.article-body :deep(h2),
.article-body :deep(h3) {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.article-body :deep(p) {
  margin-bottom: 1.2em;
}

.article-body :deep(pre) {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
}

.article-body :deep(code) {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "Consolas", monospace;
}

.article-body :deep(blockquote) {
  border-left: 4px solid #667eea;
  padding-left: 16px;
  margin: 16px 0;
  color: #666;
}

.article-body :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

.article-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border, #e1e5e9);
}

.actions {
  display: flex;
  gap: 16px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--color-bg-secondary, #f5f5f5);
  border: 1px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  color: var(--color-text, #333);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: var(--color-primary, #667eea);
  border-color: var(--color-primary, #667eea);
  color: white;
}

.action-btn.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.not-found a {
  color: #667eea;
  text-decoration: none;
}

.not-found a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .article-detail {
    padding: 16px;
  }

  .article-container {
    padding: 20px;
  }

  .article-title {
    font-size: 24px;
  }

  .article-meta {
    flex-wrap: wrap;
    gap: 12px;
  }
}
</style>
