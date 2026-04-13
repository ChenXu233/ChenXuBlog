<template>
  <div class="login-wrapper">
    <BlossomCanvas />
    <div class="login-container">
      <LiquidGlass
        border-radius="24px"
        bg-color="rgba(255, 255, 255, 0.4)"
        class="glass-panel"
      >
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
            <router-link to="/register" class="register-link-btn"
              >立即注册</router-link
            >
          </div>
        </form>
      </LiquidGlass>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive } from "vue";
import { post } from "../utils/request";
import { useRouter, useRoute } from "vue-router";
import type { UserLoginResponse } from "../types/user";
import { useAuthStore } from "../stores/authStore";
import { resetPermissionState } from "../router";
import LiquidGlass from "../components/LiquidGlass.vue";
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = reactive({
  evidence: "",
  password: "",
});

const handleLogin = () => {
  console.log("登录表单数据:", form);
  post<UserLoginResponse>("/auth/login", form).then(async (res) => {
    if (res.status === 200) {
      resetPermissionState();
      // 设置 token 和权限
      await authStore.login(res.data.access_token, res.data.refresh_token);
      // 获取用户信息
      await authStore.fetchUserInfo();
      console.log("登录成功:", res);
      const redirect = route.query.redirect as string;
      router.push(redirect || "/home");
    }
  });
};
</script>

<style scoped>
.login-wrapper {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #abb8c3 0%, #3d4a5d 100%);
}

.login-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 420px;
  z-index: 10;
  perspective: 1000px;
}

.glass-panel {
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.glass-panel:hover {
  transform: translateY(-5px) scale(1.02) rotateX(2deg) rotateY(2deg);
}

.login-form {
  padding: 2.5rem 3rem;
  width: 100%;
  box-sizing: border-box;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.nav-brand {
  display: block;
  text-align: center;
  margin-bottom: 1rem;
  color: #555;
  font-weight: 600;
  text-decoration: none;
  font-size: 0.95rem;
  transition:
    color 0.3s ease,
    transform 0.3s ease;
}

.nav-brand:hover {
  color: #222;
  transform: scale(1.05);
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 0.95rem;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.5);
  box-sizing: border-box;
  color: #333;
}

input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

input::placeholder {
  color: #666;
}

.login-btn {
  width: 100%;
  padding: 0.9rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-btn:hover {
  background: rgba(0, 0, 0, 0.85);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.register-link {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.95rem;
  color: #444;
}

.register-link-btn {
  color: #111;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.5rem;
  transition: color 0.3s ease;
}

.register-link-btn:hover {
  text-decoration: underline;
  color: #000;
}
</style>
