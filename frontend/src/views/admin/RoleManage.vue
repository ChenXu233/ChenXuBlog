<template>
  <div class="role-manage">
    <div class="toolbar">
      <h3 class="toolbar-title">角色列表</h3>
    </div>

    <div class="role-grid">
      <div class="role-card" v-for="role in roles" :key="role.id">
        <div class="role-header">
          <div class="role-info">
            <span class="role-name">{{ role.name }}</span>
            <span class="role-badge" v-if="role.is_default">默认</span>
          </div>
        </div>
        <p class="role-desc">{{ role.description || "暂无描述" }}</p>
        <div class="role-permissions">
          <span
            class="permission-tag"
            v-for="perm in role.permissions"
            :key="perm"
          >
            {{ perm }}
          </span>
          <span class="no-permission" v-if="!role.permissions.length"
            >暂无权限</span
          >
        </div>
      </div>
    </div>

    <div class="empty-state" v-if="!roles.length">暂无角色数据</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { adminService } from "../../service/admin";

interface Role {
  id: number;
  name: string;
  description: string;
  is_default: boolean;
  permissions: string[];
}

const roles = ref<Role[]>([]);

const fetchRoles = async () => {
  try {
    roles.value = await adminService.getRoles();
  } catch (error) {
    console.error("获取角色列表失败:", error);
  }
};

onMounted(() => {
  fetchRoles();
});
</script>

<style scoped>
.role-manage {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toolbar-title {
  margin: 0;
  color: #fff;
  font-size: 16px;
}

.role-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.role-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.role-card:hover {
  background: rgba(255, 255, 255, 0.06);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.role-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.role-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.role-name {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.role-badge {
  padding: 3px 8px;
  background: rgba(74, 222, 128, 0.15);
  color: #4ade80;
  border-radius: 10px;
  font-size: 11px;
}

.role-desc {
  margin: 0 0 16px 0;
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  line-height: 1.5;
}

.role-permissions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.permission-tag {
  padding: 4px 12px;
  background: rgba(244, 179, 194, 0.12);
  color: #f4b3c2;
  border-radius: 12px;
  font-size: 12px;
  font-family: "JetBrains Mono", monospace;
}

.no-permission {
  color: rgba(255, 255, 255, 0.3);
  font-size: 13px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: rgba(255, 255, 255, 0.4);
}
</style>
