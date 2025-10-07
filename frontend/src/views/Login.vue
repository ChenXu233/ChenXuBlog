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
  post<UserLoginResponse>("/auth/login", form).then((res) => {
    if (res.status === 200) {
      tokenStore.setToken(res.data.access_token);
      console.log("登录成功:", res);
      router.push("/home");
    }
  });
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-form {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2.5rem 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 420px;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform-style: preserve-3d;
}

.login-form:hover {
  transform: translateY(-5px) scale(1.01);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.nav-brand {
  display: block;
  text-align: center;
  margin-bottom: 1rem;
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
  font-size: 0.95rem;
  transition:
    color 0.3s ease,
    transform 0.3s ease;
}

.nav-brand:hover {
  color: #764ba2;
  transform: scale(1.05);
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

input {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: white;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  transform: translateY(-1px);
}

input::placeholder {
  color: #a0aec0;
  transition: color 0.3s ease;
}

input:focus::placeholder {
  color: #cbd5e0;
}

.login-btn {
  width: 100%;
  padding: 0.9rem;
  background: linear-gradient(90deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.login-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #764ba2, #667eea);
  transition: all 0.5s ease;
  z-index: -1;
}

.login-btn:hover::before {
  left: 0;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.login-btn:active {
  transform: translateY(0);
}

.register-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #666;
  font-size: 0.95rem;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
}

.register-link a::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s ease;
  border-radius: 2px;
}

.register-link a:hover {
  color: #764ba2;
}

.register-link a:hover::after {
  width: 100%;
}
</style>
