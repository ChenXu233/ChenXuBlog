<template>
  <div class="reset-container">
    <form @submit.prevent="handleSubmit" class="reset-form">
      <router-link to="/" class="nav-brand">返回首页</router-link>
      <h2>重置密码</h2>
      <p class="reset-desc">请设置您的新密码</p>

      <div class="form-group">
        <label for="password">新密码</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          minlength="6"
          placeholder="请输入新密码（至少6位）"
        />
      </div>
      <div class="form-group">
        <label for="confirm">确认密码</label>
        <input
          type="password"
          id="confirm"
          v-model="confirm"
          required
          placeholder="请再次输入新密码"
        />
      </div>

      <button type="submit" class="reset-btn" :disabled="submitting">
        {{ submitting ? "重置中..." : "重置密码" }}
      </button>

      <div v-if="message" class="success-message">{{ message }}</div>
      <div v-if="error" class="error-message">{{ error }}</div>

      <div class="back-link">
        <router-link to="/login" class="back-link">返回登录</router-link>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { authService } from "../service/auth";

const route = useRoute();
const router = useRouter();

const password = ref("");
const confirm = ref("");
const message = ref("");
const error = ref("");
const submitting = ref(false);

const token = route.query.token as string;

const handleSubmit = async () => {
  if (!password.value || password.value.length < 6) {
    error.value = "密码长度至少为6位";
    return;
  }
  if (password.value !== confirm.value) {
    error.value = "两次输入的密码不一致";
    return;
  }
  if (!token) {
    error.value = "缺少重置令牌，请从邮件中的链接进入";
    return;
  }
  submitting.value = true;
  error.value = "";
  message.value = "";
  try {
    const res = await authService.resetPassword(token, password.value);
    message.value = res.message || "密码重置成功";
    setTimeout(() => router.push("/login"), 1500);
  } catch (e: any) {
    error.value = e?.message || "重置失败，链接可能已过期";
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.reset-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}
.reset-form {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2.5rem 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 420px;
}
.reset-form h2 {
  margin-bottom: 8px;
  color: #333;
  text-align: center;
}
.reset-desc {
  color: #777;
  font-size: 14px;
  text-align: center;
  margin-bottom: 24px;
}
.nav-brand {
  display: block;
  text-align: center;
  color: #764ba2;
  text-decoration: none;
  font-size: 14px;
  margin-bottom: 16px;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #555;
}
.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.form-group input:focus {
  border-color: #764ba2;
}
.reset-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.reset-btn:hover {
  opacity: 0.9;
}
.reset-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.success-message {
  margin-top: 14px;
  padding: 10px;
  background: #d4edda;
  color: #155724;
  border-radius: 8px;
  font-size: 13px;
  text-align: center;
}
.error-message {
  margin-top: 14px;
  padding: 10px;
  background: #f8d7da;
  color: #721c24;
  border-radius: 8px;
  font-size: 13px;
  text-align: center;
}
.back-link {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
  color: #764ba2;
  text-decoration: none;
  display: block;
}
</style>
