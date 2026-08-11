<template>
  <div class="forgot-container">
    <form @submit.prevent="handleSubmit" class="forgot-form">
      <router-link to="/" class="nav-brand">返回首页</router-link>
      <h2>找回密码</h2>
      <p class="forgot-desc">输入注册邮箱，我们将发送密码重置链接</p>

      <div class="form-group">
        <label for="email">邮箱</label>
        <input
          type="email"
          id="email"
          v-model="email"
          required
          placeholder="请输入注册邮箱"
        />
      </div>

      <button type="submit" class="forgot-btn" :disabled="submitting">
        {{ submitting ? "发送中..." : "发送重置链接" }}
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
import { authService } from "../service/auth";

const email = ref("");
const message = ref("");
const error = ref("");
const submitting = ref(false);

const handleSubmit = async () => {
  if (!email.value.trim()) return;
  submitting.value = true;
  error.value = "";
  message.value = "";
  try {
    const res = await authService.forgotPassword(email.value.trim());
    message.value = res.message || "重置链接已发送，请查收邮件";
  } catch (e: any) {
    error.value = e?.message || "发送失败，请稍后重试";
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.forgot-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}
.forgot-form {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2.5rem 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 420px;
}
.forgot-form h2 {
  margin-bottom: 8px;
  color: #333;
  text-align: center;
}
.forgot-desc {
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
.forgot-btn {
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
.forgot-btn:hover {
  opacity: 0.9;
}
.forgot-btn:disabled {
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
