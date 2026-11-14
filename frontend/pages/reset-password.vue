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
definePageMeta({ layout: false });
useSeo({ title: "重置密码", noindex: true });

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
