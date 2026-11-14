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
definePageMeta({ layout: false });
useSeo({ title: "找回密码", noindex: true });

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
