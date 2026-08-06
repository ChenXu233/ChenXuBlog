<template>
  <div class="comment-manage">
    <!-- 评论列表 -->
    <div class="comment-table">
      <div class="table-header">
        <span class="col-id">ID</span>
        <span class="col-content">内容</span>
        <span class="col-user">用户</span>
        <span class="col-blog">文章</span>
        <span class="col-time">时间</span>
        <span class="col-actions">操作</span>
      </div>

      <div class="table-body">
        <div class="table-row" v-for="comment in comments" :key="comment.id">
          <span class="col-id">{{ comment.id }}</span>
          <div class="col-content">
            <span class="content-text">{{ comment.content }}</span>
          </div>
          <span class="col-user">@{{ comment.username }}</span>
          <span class="col-blog">{{ comment.blog_title }}</span>
          <span class="col-time">{{ formatTime(comment.created_at) }}</span>
          <div class="col-actions">
            <button class="action-btn delete" @click="confirmDelete(comment)">
              删除
            </button>
          </div>
        </div>

        <div class="empty-state" v-if="!comments.length">暂无评论</div>
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

interface Comment {
  id: number;
  blog_id: number;
  blog_title: string;
  user_id: number;
  username: string;
  content: string;
  created_at: number;
  updated_at: number;
}

const comments = ref<Comment[]>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

const totalPages = computed(() => Math.ceil(total.value / pageSize.value) || 1);

const formatTime = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleDateString("zh-CN");
};

const fetchComments = async () => {
  try {
    const data = await adminService.getComments(
      currentPage.value,
      pageSize.value,
    );
    comments.value = data.items;
    total.value = data.total;
  } catch (error) {
    showError("获取评论列表失败");
  }
};

const confirmDelete = async (comment: Comment) => {
  if (!confirm(`确定删除这条评论吗？此操作不可恢复。`)) return;
  try {
    await adminService.deleteComment(comment.id);
    showSuccess("评论已删除");
    fetchComments();
  } catch (error) {
    showError("删除失败");
  }
};

watch(currentPage, () => {
  fetchComments();
});

onMounted(() => {
  fetchComments();
});
</script>

<style scoped>
.comment-manage {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 表格 */
.comment-table {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 50px 1fr 100px 150px 100px 80px;
  gap: 12px;
  padding: 14px 20px;
  background: rgba(255, 255, 255, 0.05);
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.table-row {
  display: grid;
  grid-template-columns: 50px 1fr 100px 150px 100px 80px;
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

.col-content {
  min-width: 0;
}

.content-text {
  color: #fff;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.col-user {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
}

.col-blog {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.col-time {
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
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
