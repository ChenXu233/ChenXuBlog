<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <router-link to="/" class="nav-brand">返回首页</router-link>
      <h2>用户登录</h2>

      <div class="form-group">
        <label for="evidence">用户名或邮箱</label>
        <input
          type="text"
          id="evidence"
          v-model="form.evidence"
          required
          placeholder="请输入用户名或邮箱"
        />
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input
          type="password"
          id="password"
          v-model="form.password"
          required
          placeholder="请输入密码"
        />
      </div>

      <button type="submit" class="login-btn">登录</button>

      <div class="register-link">
        <span>没有账号？</span>
        <router-link to="/register" class="register-link">立即注册</router-link>
      </div>
    </form>
  </div>
</template>
<script setup lang="ts">
definePageMeta({ layout: false });
useSeo({ title: "登录", noindex: true });

import { reactive } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "../composables/useAuth";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = reactive({
  evidence: "",
  password: "",
});

const handleLogin = async () => {
  try {
    await authStore.login(form.evidence, form.password);
    const redirect = route.query.redirect as string;
    router.push(redirect || "/home");
  } catch (e) {
    console.error("登录失败:", e);
  }
};
</script>
