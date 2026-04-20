<template>
  <div class="user-profile">
    <div v-if="loading" class="loading">
      <i class="fa fa-spinner fa-spin"></i> 加载中...
    </div>

    <div v-else-if="user" class="profile-container">
      <div class="profile-header">
        <el-avatar :src="user.avatar" :size="100" />
        <div class="user-info">
          <h1 class="username">{{ user.username }}</h1>
          <p class="email">{{ user.email }}</p>
        </div>
        <button
          v-if="isOwnProfile"
          @click="showEditDialog = true"
          class="edit-btn"
        >
          <i class="fa fa-edit"></i> 编辑资料
        </button>
      </div>

      <div class="profile-stats">
        <div class="stat-item">
          <span class="stat-value">{{ articles?.length ?? 0 }}</span>
          <span class="stat-label">文章</span>
        </div>
      </div>

      <div class="articles-section">
        <h2>他的文章</h2>
        <div v-if="!articles?.length" class="empty-state">暂无文章</div>
        <div v-else class="articles-grid">
          <BlogCard
            v-for="article in articles || []"
            :key="article.id"
            :article="article"
          />
        </div>
        <div v-if="totalPages > 1" class="pagination">
          <button
            v-for="page in totalPages"
            :key="page"
            @click="fetchUserArticles(page)"
            :class="{ active: currentPage === page }"
            class="page-btn"
          >
            {{ page }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <h2>用户不存在</h2>
      <router-link to="/home">返回首页</router-link>
    </div>

    <!-- 编辑资料弹窗 -->
    <div
      v-if="showEditDialog"
      class="edit-dialog-overlay"
      @click.self="showEditDialog = false"
    >
      <div class="edit-dialog">
        <h3>编辑资料</h3>
        <div class="form-group">
          <label>用户名</label>
          <input v-model="editForm.username" type="text" />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="editForm.email" type="email" />
        </div>
        <div class="form-group">
          <label>头像 URL</label>
          <input v-model="editForm.avatar" type="text" />
        </div>
        <div class="dialog-actions">
          <button @click="showEditDialog = false" class="cancel-btn">
            取消
          </button>
          <button @click="handleUpdate" class="save-btn" :disabled="saving">
            {{ saving ? "保存中..." : "保存" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { userService } from "../service/user";
import { useUserStore } from "../stores/userStore";
import { useTokenStore } from "../stores/token";
import { showError } from "../utils/request";
import BlogCard from "../components/BlogCard.vue";
import type { User, UserUpdate } from "../types/user";
import type { Article } from "../types/article";

const route = useRoute();
const userStore = useUserStore();
const tokenStore = useTokenStore();

const user = ref<User | null>(null);
const articles = ref<Article[]>([]);
const loading = ref(true);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const showEditDialog = ref(false);
const saving = ref(false);

const editForm = ref<{
  username: string;
  email: string;
  avatar: string;
}>({
  username: "",
  email: "",
  avatar: "",
});

const isOwnProfile = computed(() => {
  return tokenStore.isAuthenticated && userStore.id === route.params.id;
});

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value);
});

const fetchUserInfo = async () => {
  loading.value = true;
  try {
    user.value = await userService.getUserInfo(route.params.id as string);
    editForm.value = {
      username: user.value.username,
      email: user.value.email,
      avatar: user.value.avatar || "",
    };
  } catch (error) {
    showError("加载用户信息失败");
  } finally {
    loading.value = false;
  }
};

const fetchUserArticles = async (page = 1) => {
  currentPage.value = page;
  try {
    const data = await userService.getUserBlogs({
      user_id: route.params.id as string,
      page,
      page_size: pageSize.value,
    });
    articles.value = data.articles;
    total.value = data.total;
  } catch (error) {
    showError("加载文章列表失败");
  }
};

const handleUpdate = async () => {
  if (!user.value) return;
  saving.value = true;
  try {
    const data: UserUpdate = {
      username: editForm.value.username,
      email: editForm.value.email,
      avatar: editForm.value.avatar,
    };
    const updated = await userService.updateUserInfo(user.value.uuid, data);
    user.value = updated;
    userStore.setUserInfo({
      id: updated.uuid,
      name: updated.username,
    });
    showEditDialog.value = false;
    showError("保存成功", "提示", "success");
  } catch (error) {
    showError("保存失败");
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  fetchUserInfo();
  fetchUserArticles();
});
</script>

<style scoped>
.user-profile {
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

.profile-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
}

.user-info {
  flex: 1;
}

.username {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.email {
  color: #999;
  font-size: 14px;
  margin: 0;
}

.edit-btn {
  padding: 10px 20px;
  background: var(--color-primary, #667eea);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.profile-stats {
  display: flex;
  gap: 32px;
  padding: 24px 0;
  border-top: 1px solid var(--color-border, #e1e5e9);
  border-bottom: 1px solid var(--color-border, #e1e5e9);
  margin-bottom: 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary, #667eea);
}

.stat-label {
  font-size: 14px;
  color: #999;
}

.articles-section h2 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: #999;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
}

.page-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-border, #e1e5e9);
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover {
  background: var(--color-bg-secondary, #f5f5f5);
}

.page-btn.active {
  background: var(--color-primary, #667eea);
  border-color: var(--color-primary, #667eea);
  color: white;
}

/* 编辑弹窗 */
.edit-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.edit-dialog {
  background: white;
  border-radius: 16px;
  padding: 32px;
  width: 90%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.edit-dialog h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 24px 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary, #667eea);
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn,
.save-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: var(--color-bg-secondary, #f5f5f5);
  border: 1px solid var(--color-border, #e1e5e9);
  color: var(--color-text, #333);
}

.save-btn {
  background: var(--color-primary, #667eea);
  border: none;
  color: white;
}

.save-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.not-found a {
  color: var(--color-primary, #667eea);
  text-decoration: none;
}

.not-found a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
