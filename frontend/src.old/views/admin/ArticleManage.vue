<template>
  <div class="article-manage">
    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="filter-tabs">
        <button
          class="tab-btn"
          :class="{ active: filter === null }"
          @click="filter = null"
        >
          全部
        </button>
        <button
          class="tab-btn"
          :class="{ active: filter === true }"
          @click="filter = true"
        >
          已发布
        </button>
        <button
          class="tab-btn"
          :class="{ active: filter === false }"
          @click="filter = false"
        >
          草稿
        </button>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="article-table">
      <div class="table-header">
        <span class="col-id">ID</span>
        <span class="col-title">标题</span>
        <span class="col-author">作者</span>
        <span class="col-tags">标签</span>
        <span class="col-stats">数据</span>
        <span class="col-status">状态</span>
        <span class="col-time">时间</span>
        <span class="col-actions">操作</span>
      </div>

      <div class="table-body">
        <div class="table-row" v-for="article in articles" :key="article.id">
          <span class="col-id">{{ article.id }}</span>
          <div class="col-title">
            <span class="title-text">{{ article.title }}</span>
          </div>
          <span class="col-author">@{{ article.username }}</span>
          <div class="col-tags">
            <span
              class="tag"
              v-for="tag in article.tags_name?.slice(0, 2)"
              :key="tag"
            >
              {{ tag }}
            </span>
          </div>
          <div class="col-stats">
            <span class="stat">👁 {{ article.view_count }}</span>
            <span class="stat">❤️ {{ article.likes_count }}</span>
          </div>
          <div class="col-status">
            <span
              class="status-badge"
              :class="article.published ? 'published' : 'draft'"
            >
              {{ article.published ? "已发布" : "草稿" }}
            </span>
          </div>
          <span class="col-time">{{ formatTime(article.created_at) }}</span>
          <div class="col-actions">
            <button class="action-btn toggle" @click="togglePublish(article)">
              {{ article.published ? "撤回" : "发布" }}
            </button>
            <router-link
              :to="`/article/edit/${article.id}`"
              class="action-btn edit"
            >
              编辑
            </router-link>
            <button class="action-btn delete" @click="confirmDelete(article)">
              删除
            </button>
          </div>
        </div>

        <div class="empty-state" v-if="!articles.length">暂无文章</div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="currentPage--"
      >
        上一页
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { adminService } from "../../service/admin";
import { showError, showSuccess } from "../../utils/request";

interface Article {
  id: number;
  user_uuid: string;
  username: string;
  title: string;
  cover_url: string;
  tags_name: string[];
  created_at: number;
  updated_at: number;
  view_count: number;
  likes_count: number;
  published: boolean;
}

const articles = ref<Article[]>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const filter = ref<boolean | null>(null);

const totalPages = computed(() => Math.ceil(total.value / pageSize.value) || 1);

const formatTime = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleDateString("zh-CN");
};

const fetchArticles = async () => {
  try {
    const data = await adminService.getArticles(
      currentPage.value,
      pageSize.value,
      filter.value ?? undefined,
    );
    articles.value = data.items;
    total.value = data.total;
  } catch (error) {
    showError("获取文章列表失败");
  }
};

const togglePublish = async (article: Article) => {
  try {
    await adminService.toggleBlogPublish(article.id);
    showSuccess(article.published ? "已撤回发布" : "已发布");
    fetchArticles();
  } catch (error) {
    showError("操作失败");
  }
};

const confirmDelete = async (article: Article) => {
  if (!confirm(`确定删除文章《${article.title}》吗？此操作不可恢复。`)) return;
  try {
    await adminService.deleteBlog(article.id);
    showSuccess("文章已删除");
    fetchArticles();
  } catch (error) {
    showError("删除失败");
  }
};

watch([currentPage, filter], () => {
  fetchArticles();
});

onMounted(() => {
  fetchArticles();
});
</script>

<style scoped>
.article-manage {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toolbar {
  display: flex;
  gap: 16px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.03);
  padding: 6px;
  border-radius: 10px;
}

.tab-btn {
  padding: 8px 16px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #fff;
}

.tab-btn.active {
  background: rgba(244, 179, 194, 0.2);
  color: #f4b3c2;
}

/* 表格 */
.article-table {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 50px 1fr 100px 120px 100px 70px 100px 150px;
  gap: 12px;
  padding: 14px 20px;
  background: rgba(255, 255, 255, 0.05);
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.table-row {
  display: grid;
  grid-template-columns: 50px 1fr 100px 120px 100px 70px 100px 150px;
  gap: 12px;
  padding: 14px 20px;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  transition: background 0.2s;
}

.table-row:hover {
  background: rgba(255, 255, 255, 0.03);
}

.table-row:last-child {
  border-bottom: none;
}

.col-id {
  font-family: "JetBrains Mono", monospace;
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
}

.col-title {
  min-width: 0;
}

.title-text {
  color: #fff;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.col-author {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
}

.col-tags {
  display: flex;
  gap: 6px;
}

.tag {
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
  border-radius: 8px;
  font-size: 11px;
}

.col-stats {
  display: flex;
  gap: 10px;
}

.stat {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.col-time {
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
}

.status-badge {
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 11px;
}

.status-badge.published {
  background: rgba(74, 222, 128, 0.12);
  color: #4ade80;
}

.status-badge.draft {
  background: rgba(255, 213, 71, 0.12);
  color: #ffd547;
}

.col-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.action-btn.toggle {
  background: rgba(74, 222, 128, 0.12);
  color: #4ade80;
}

.action-btn.toggle:hover {
  background: rgba(74, 222, 128, 0.2);
}

.action-btn.edit {
  background: rgba(244, 179, 194, 0.12);
  color: #f4b3c2;
}

.action-btn.edit:hover {
  background: rgba(244, 179, 194, 0.2);
}

.action-btn.delete {
  background: rgba(255, 107, 107, 0.12);
  color: #ff6b6b;
}

.action-btn.delete:hover {
  background: rgba(255, 107, 107, 0.2);
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: rgba(255, 255, 255, 0.4);
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.page-btn {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}
</style>
