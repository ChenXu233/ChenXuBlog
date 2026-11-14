<template>
  <div class="register-container">
    <form @submit.prevent="handleRegister" class="register-form">
      <router-link to="/" class="nav-brand">返回首页</router-link>
      <h2>用户注册</h2>

      <div class="form-group">
        <label for="username">用户名</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          required
          placeholder="请输入用户名"
        />
        <div v-if="errors.username" class="error-message">
          {{ errors.username }}
        </div>
      </div>

      <div class="form-group">
        <label for="email">邮箱</label>
        <input
          type="email"
          id="email"
          v-model="form.email"
          required
          placeholder="请输入邮箱"
        />
        <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input
          type="password"
          id="password"
          v-model="form.password"
          required
          placeholder="请输入密码（至少6位）"
        />
        <div v-if="errors.password" class="error-message">
          {{ errors.password }}
        </div>
      </div>

      <button type="submit" class="register-btn" :disabled="isSubmitting">
        {{ isSubmitting ? "注册中..." : "注册" }}
      </button>

      <div class="login-link">
        <span>已有账号？</span>
        <router-link to="/login" class="login-link">立即登录</router-link>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false });
useSeo({ title: "注册", noindex: true });

import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { authService } from "../service/auth";

const router = useRouter();
const form = reactive({
  username: "",
  email: "",
  password: "",
});
const errors = reactive({
  username: "",
  email: "",
  password: "",
});
const isSubmitting = ref(false);

// 表单验证
const validateForm = () => {
  let isValid = true;

  // 重置错误信息
  errors.username = "";
  errors.email = "";
  errors.password = "";

  // 验证用户名
  if (!form.username.trim()) {
    errors.username = "用户名不能为空";
    isValid = false;
  } else if (form.username.length < 2 || form.username.length > 20) {
    errors.username = "用户名长度应在2-20个字符之间";
    isValid = false;
  }

  // 验证邮箱
  const emailRegex = /^[^\n\s@]+@[^\n\s@]+\.[^\n\s@]+$/;
  if (!form.email.trim()) {
    errors.email = "邮箱不能为空";
    isValid = false;
  } else if (!emailRegex.test(form.email)) {
    errors.email = "请输入有效的邮箱地址";
    isValid = false;
  }

  // 验证密码
  if (!form.password) {
    errors.password = "密码不能为空";
    isValid = false;
  } else if (form.password.length < 6) {
    errors.password = "密码长度至少为6位";
    isValid = false;
  }

  return isValid;
};

const handleRegister = async () => {
  if (!validateForm()) {
    return;
  }
  try {
    await authService.register({
      username: form.username,
      email: form.email,
      password: form.password,
    });
    // 注册成功：提示邮箱验证，跳转登录
    router.push("/login?registered=1");
  } catch (e: any) {
    errors.password = e?.message || "注册失败，请稍后重试";
  }
};
</script>
