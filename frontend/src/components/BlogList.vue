<template>
  <div class="blog-list">
    <div class="list-header">
      <h2 class="list-title">
        <i class="fa fa-newspaper-o"></i>
        {{ title }}
      </h2>
      <div class="search-box">
        <input
          v-model="keyword"
          type="text"
          placeholder="搜索文章..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" class="search-btn">
          <i class="fa fa-search"></i>
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <i class="fa fa-spinner fa-spin"></i> 加载中...
    </div>

    <div v-else-if="articles.length === 0" class="empty-state">
      <p>暂无文章</p>
    </div>

    <div v-else class="articles-grid">
      <BlogCard v-for="article in articles" :key="article.id" :article="article" />
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="page-btn prev"
      >
        <i class="fa fa-chevron-left"></i>
      </button>
      <button
        v-for="page in visiblePages"
        :key="page"
        @click="goToPage(page)"
        :class="{ active: currentPage === page }"
        class="page-btn"
      >
        {{ page }}
      </button>
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="page-btn next"
      >
        <i class="fa fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { blogService } from "../service/blog";
import BlogCard from "./BlogCard.vue";
import type { Article } from "../types/article";

const props = withDefaults(
  defineProps<{
    title?: string;
    userId?: string;
    tag?: string;
  }>(),
  {
    title: "文章列表",
  }
);

const articles = ref<Article[]>([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(12);
const total = ref(0);
const keyword = ref("");

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value);
});

const visiblePages = computed(() => {
  const pages: number[] = [];
  const maxVisible = 5;
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
  let end = Math.min(totalPages.value, start + maxVisible - 1);

  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1);
  }

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

const fetchArticles = async (page = 1) => {
  loading.value = true;
  currentPage.value = page;
  try {
    const params: any = {
      page,
      page_size: pageSize.value,
    };
    if (props.userId) {
      params.user_id = props.userId;
    }
    if (props.tag) {
      params.tag = props.tag;
    }
    if (keyword.value) {
      params.keyword = keyword.value;
    }
    const data = await blogService.getBlogList(params);
    articles.value = data.articles;
    total.value = data.total;
  } catch (error) {
    console.error("加载文章列表失败:", error);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  fetchArticles(1);
};

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  fetchArticles(page);
  window.scrollTo({ top: 0, behavior: "smooth" });
};

onMounted(() => {
  fetchArticles();
});

watch(
  () => [props.userId, props.tag],
  () => {
    fetchArticles(1);
  }
);
</script>

<style scoped>
.blog-list {
  padding: 40px 0;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.list-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.list-title i {
  color: #667eea;
}

.search-box {
  display: flex;
  gap: 8px;
}

.search-box input {
  padding: 10px 16px;
  border: 1px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  font-size: 14px;
  width: 200px;
  transition: border-color 0.2s;
}

.search-box input:focus {
  outline: none;
  border-color: #667eea;
}

.search-btn {
  padding: 10px 16px;
  background: #667eea;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.search-btn:hover {
  background: #5a6fd6;
}

.loading,
.empty-state {
  text-align: center;
  padding: 64px 24px;
  color: #999;
}

.loading i {
  font-size: 24px;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 40px;
}

.page-btn {
  min-width: 40px;
  height: 40px;
  padding: 0 12px;
  border: 1px solid var(--color-border, #e1e5e9);
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover:not(:disabled) {
  background: var(--color-bg-secondary, #f5f5f5);
  border-color: #667eea;
}

.page-btn.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .list-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-box input {
    width: 150px;
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
