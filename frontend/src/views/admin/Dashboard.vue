<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.label">
        <div class="stat-icon">{{ stat.icon }}</div>
        <div class="stat-info">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
        <div class="stat-change" :class="stat.changeClass" v-if="stat.change">
          {{ stat.change }}
        </div>
      </div>
    </div>

    <!-- 今日动态 -->
    <div class="today-section">
      <h3 class="section-title">今日动态</h3>
      <div class="today-cards">
        <div class="today-card">
          <span class="today-icon">📝</span>
          <div class="today-info">
            <span class="today-value">{{ statsData.total_blogs_today }}</span>
            <span class="today-label">篇新文章</span>
          </div>
        </div>
        <div class="today-card">
          <span class="today-icon">💬</span>
          <div class="today-info">
            <span class="today-value">{{
              statsData.total_comments_today
            }}</span>
            <span class="today-label">条新评论</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近内容 -->
    <div class="recent-section">
      <div class="recent-block">
        <h3 class="section-title">最近文章</h3>
        <div class="recent-list">
          <div
            class="recent-item"
            v-for="blog in statsData.recent_blogs"
            :key="blog.id"
          >
            <div class="recent-info">
              <span class="recent-title">{{ blog.title }}</span>
              <span class="recent-meta">
                <span class="author">@{{ blog.username }}</span>
                <span class="views">👁 {{ blog.view_count }}</span>
                <span class="likes">❤️ {{ blog.likes_count }}</span>
              </span>
            </div>
            <span class="recent-time">{{ formatTime(blog.created_at) }}</span>
          </div>
          <div class="empty-state" v-if="!statsData.recent_blogs?.length">
            暂无文章
          </div>
        </div>
      </div>

      <div class="recent-block">
        <h3 class="section-title">最近评论</h3>
        <div class="recent-list">
          <div
            class="recent-item"
            v-for="comment in statsData.recent_comments"
            :key="comment.id"
          >
            <div class="recent-info">
              <span class="recent-content">{{ comment.content }}</span>
              <span class="recent-meta">
                <span class="author">@{{ comment.username }}</span>
                <span class="blog">文章: {{ comment.blog_title }}</span>
              </span>
            </div>
            <span class="recent-time">{{
              formatTime(comment.created_at)
            }}</span>
          </div>
          <div class="empty-state" v-if="!statsData.recent_comments?.length">
            暂无评论
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { adminService } from "../../service/admin";

const statsData = reactive({
  total_users: 0,
  total_blogs: 0,
  total_comments: 0,
  total_blogs_today: 0,
  total_comments_today: 0,
  recent_blogs: [] as any[],
  recent_comments: [] as any[],
});

const stats = ref([
  { label: "用户总数", value: "0", icon: "👥", change: "", changeClass: "" },
  { label: "文章总数", value: "0", icon: "📝", change: "", changeClass: "" },
  { label: "评论总数", value: "0", icon: "💬", change: "", changeClass: "" },
]);

const formatTime = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes} 分钟前`;
  if (hours < 24) return `${hours} 小时前`;
  if (days < 7) return `${days} 天前`;
  return date.toLocaleDateString("zh-CN");
};

const fetchStats = async () => {
  try {
    const data = await adminService.getStats();
    statsData.total_users = data.total_users;
    statsData.total_blogs = data.total_blogs;
    statsData.total_comments = data.total_comments;
    statsData.total_blogs_today = data.total_blogs_today;
    statsData.total_comments_today = data.total_comments_today;
    statsData.recent_blogs = data.recent_blogs;
    statsData.recent_comments = data.recent_comments;

    stats.value = [
      {
        label: "用户总数",
        value: data.total_users.toString(),
        icon: "👥",
        change: "",
        changeClass: "",
      },
      {
        label: "文章总数",
        value: data.total_blogs.toString(),
        icon: "📝",
        change: "",
        changeClass: "",
      },
      {
        label: "评论总数",
        value: data.total_comments.toString(),
        icon: "💬",
        change: "",
        changeClass: "",
      },
    ];
  } catch (error) {
    console.error("获取统计数据失败:", error);
  }
};

onMounted(() => {
  fetchStats();
});
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.stat-icon {
  font-size: 40px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(244, 179, 194, 0.15);
  border-radius: 16px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  font-family: "JetBrains Mono", monospace;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  font-family: "PingFang SC", sans-serif;
}

.stat-change {
  margin-left: auto;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 20px;
}

.stat-change.positive {
  background: rgba(74, 222, 128, 0.15);
  color: #4ade80;
}

.stat-change.negative {
  background: rgba(255, 107, 107, 0.15);
  color: #ff6b6b;
}

/* 今日动态 */
.today-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 20px 0;
  font-family: "PingFang SC", sans-serif;
}

.today-cards {
  display: flex;
  gap: 20px;
}

.today-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
}

.today-icon {
  font-size: 32px;
}

.today-info {
  display: flex;
  flex-direction: column;
}

.today-value {
  font-size: 28px;
  font-weight: 700;
  color: #f4b3c2;
  font-family: "JetBrains Mono", monospace;
}

.today-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  font-family: "PingFang SC", sans-serif;
}

/* 最近内容 */
.recent-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.recent-block {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 24px;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  transition: background 0.2s;
}

.recent-item:hover {
  background: rgba(255, 255, 255, 0.06);
}

.recent-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.recent-title,
.recent-content {
  font-size: 14px;
  color: #fff;
  font-family: "PingFang SC", sans-serif;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recent-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.recent-meta .author {
  color: #f4b3c2;
}

.recent-time {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  white-space: nowrap;
  margin-left: 12px;
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 14px;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .recent-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
