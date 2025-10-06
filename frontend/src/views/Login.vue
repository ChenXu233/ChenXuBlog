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
        <a href="/register">立即注册</a>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { post } from "../utils/request";
import { useRouter } from "vue-router";
import type { UserLoginResponse } from "../types/user";
import { useTokenStore } from "../stores/token";

const router = useRouter();
const tokenStore = useTokenStore();

const form = reactive({
  evidence: "",
  password: "",
});

const handleLogin = () => {
  console.log("登录表单数据:", form);
  post<UserLoginResponse>("/auth/login", form)
    .then((res) => {
      if (res.status === 200) {
        tokenStore.setToken(res.data.access_token);
        console.log("登录成功:", res);
        router.push("/home");
      }
    })
    .catch((err) => {
      console.error("登录失败:", err.response.data.detail);
    });
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.login-form {
  background: white;
  padding: 2rem 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

.login-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-btn:hover {
  background-color: #337ecc;
}

.register-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}

.register-link a {
  color: #409eff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
