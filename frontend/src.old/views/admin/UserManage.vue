<template>
  <div class="user-manage">
    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="search-box">
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="搜索用户名或邮箱..."
          class="search-input"
        />
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="user-table">
      <div class="table-header">
        <span class="col-id">ID</span>
        <span class="col-user">用户</span>
        <span class="col-email">邮箱</span>
        <span class="col-roles">角色</span>
        <span class="col-status">状态</span>
        <span class="col-time">注册时间</span>
        <span class="col-actions">操作</span>
      </div>

      <div class="table-body">
        <div class="table-row" v-for="user in filteredUsers" :key="user.id">
          <span class="col-id">{{ user.id }}</span>
          <div class="col-user">
            <el-avatar
              :size="32"
              :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username}`"
            />
            <span class="username">{{ user.username }}</span>
          </div>
          <span class="col-email">{{ user.email }}</span>
          <div class="col-roles">
            <span class="role-tag" v-for="role in user.roles" :key="role">
              {{ role }}
            </span>
          </div>
          <div class="col-status">
            <span
              class="status-badge"
              :class="user.is_verified ? 'verified' : 'unverified'"
            >
              {{ user.is_verified ? "已验证" : "未验证" }}
            </span>
          </div>
          <span class="col-time">{{ formatTime(user.created_at) }}</span>
          <div class="col-actions">
            <button class="action-btn edit" @click="openRoleDialog(user)">
              编辑角色
            </button>
            <button class="action-btn delete" @click="confirmDelete(user)">
              删除
            </button>
          </div>
        </div>

        <div class="empty-state" v-if="!filteredUsers.length">暂无用户</div>
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

    <!-- 角色编辑对话框 -->
    <div
      class="dialog-overlay"
      v-if="showRoleDialog"
      @click.self="showRoleDialog = false"
    >
      <div class="dialog">
        <div class="dialog-header">
          <h3>编辑用户角色 - {{ selectedUser?.username }}</h3>
          <button class="close-btn" @click="showRoleDialog = false">×</button>
        </div>
        <div class="dialog-body">
          <div class="role-select">
            <label
              class="role-checkbox"
              v-for="role in allRoles"
              :key="role.id"
            >
              <input
                type="checkbox"
                :value="role.id"
                v-model="selectedRoleIds"
              />
              <span class="role-name">{{ role.name }}</span>
              <span class="role-desc">{{ role.description }}</span>
            </label>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="showRoleDialog = false">
            取消
          </button>
          <button class="confirm-btn" @click="updateUserRole">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { adminService } from "../../service/admin";
import { showError, showSuccess } from "../../utils/request";

interface User {
  id: number;
  uuid: string;
  username: string;
  email: string;
  is_verified: boolean;
  created_at: number;
  roles: string[];
}

interface Role {
  id: number;
  name: string;
  description: string;
  is_default: boolean;
}

const users = ref<User[]>([]);
const allRoles = ref<Role[]>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const searchKeyword = ref("");
const showRoleDialog = ref(false);
const selectedUser = ref<User | null>(null);
const selectedRoleIds = ref<number[]>([]);

const totalPages = computed(() => Math.ceil(total.value / pageSize.value) || 1);

const filteredUsers = computed(() => {
  if (!searchKeyword.value) return users.value;
  const keyword = searchKeyword.value.toLowerCase();
  return users.value.filter(
    (u) =>
      u.username.toLowerCase().includes(keyword) ||
      u.email.toLowerCase().includes(keyword),
  );
});

const formatTime = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleDateString("zh-CN");
};

const fetchUsers = async () => {
  try {
    const data = await adminService.getUsers(currentPage.value, pageSize.value);
    users.value = data.items;
    total.value = data.total;
  } catch (error) {
    showError("获取用户列表失败");
  }
};

const fetchRoles = async () => {
  try {
    allRoles.value = await adminService.getRoles();
  } catch (error) {
    showError("获取角色列表失败");
  }
};

const openRoleDialog = (user: User) => {
  selectedUser.value = user;
  // 将角色名转换为ID
  selectedRoleIds.value = allRoles.value
    .filter((r) => user.roles.includes(r.name))
    .map((r) => r.id);
  showRoleDialog.value = true;
};

const updateUserRole = async () => {
  if (!selectedUser.value) return;
  try {
    await adminService.updateUserRole(
      selectedUser.value.id,
      selectedRoleIds.value,
    );
    showSuccess("角色更新成功");
    showRoleDialog.value = false;
    fetchUsers();
  } catch (error) {
    showError("角色更新失败");
  }
};

const confirmDelete = async (user: User) => {
  if (!confirm(`确定删除用户 ${user.username} 吗？此操作不可恢复。`)) return;
  try {
    await adminService.deleteUser(user.id);
    showSuccess("用户已删除");
    fetchUsers();
  } catch (error) {
    showError("删除失败");
  }
};

watch(currentPage, () => {
  fetchUsers();
});

onMounted(() => {
  fetchUsers();
  fetchRoles();
});
</script>

<style scoped>
.user-manage {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toolbar {
  display: flex;
  gap: 16px;
}

.search-box {
  flex: 1;
}

.search-input {
  width: 100%;
  max-width: 320px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.search-input:focus {
  outline: none;
  border-color: #f4b3c2;
}

/* 表格 */
.user-table {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 60px 180px 200px 150px 80px 120px 140px;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.05);
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.table-row {
  display: grid;
  grid-template-columns: 60px 180px 200px 150px 80px 120px 140px;
  gap: 16px;
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
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
}

.col-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  color: #fff;
  font-size: 14px;
}

.col-email {
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.col-roles {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.role-tag {
  padding: 3px 10px;
  background: rgba(244, 179, 194, 0.15);
  color: #f4b3c2;
  border-radius: 12px;
  font-size: 12px;
}

.col-time {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
}

.status-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.status-badge.verified {
  background: rgba(74, 222, 128, 0.15);
  color: #4ade80;
}

.status-badge.unverified {
  background: rgba(255, 107, 107, 0.15);
  color: #ff6b6b;
}

.col-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.edit {
  background: rgba(244, 179, 194, 0.15);
  color: #f4b3c2;
}

.action-btn.edit:hover {
  background: rgba(244, 179, 194, 0.25);
}

.action-btn.delete {
  background: rgba(255, 107, 107, 0.15);
  color: #ff6b6b;
}

.action-btn.delete:hover {
  background: rgba(255, 107, 107, 0.25);
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

/* 对话框 */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  width: 420px;
  background: #1a1a2e;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.dialog-header h3 {
  margin: 0;
  color: #fff;
  font-size: 16px;
}

.close-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 18px;
}

.dialog-body {
  padding: 24px;
}

.role-select {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.role-checkbox:hover {
  background: rgba(255, 255, 255, 0.06);
}

.role-checkbox input {
  width: 18px;
  height: 18px;
  accent-color: #f4b3c2;
}

.role-name {
  color: #fff;
  font-weight: 500;
}

.role-desc {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
  margin-left: auto;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cancel-btn,
.confirm-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.7);
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.confirm-btn {
  background: #f4b3c2;
  color: #1a1a2e;
  font-weight: 500;
}

.confirm-btn:hover {
  opacity: 0.9;
}
</style>
