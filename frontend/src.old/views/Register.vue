<template>
  <div class="register-wrapper">
    <BlossomCanvas />
    <div class="register-container">
      <LiquidGlass
        border-radius="24px"
        bg-color="rgba(255, 255, 255, 0.4)"
        class="glass-panel"
      >
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
            <div v-if="errors.email" class="error-message">
              {{ errors.email }}
            </div>
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

          <div class="login-link-container">
            <span>已有账号？</span>
            <router-link to="/login" class="login-link">立即登录</router-link>
          </div>
        </form>
      </LiquidGlass>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { post } from "../utils/request";
import type { UserRegisterResponse } from "../types/user";
import LiquidGlass from "../components/LiquidGlass.vue";
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";

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

const handleRegister = () => {
  if (!validateForm()) {
    return;
  }
  post<UserRegisterResponse>("/register", form).then((res) => {
    if (res.status === 200) {
      router.push("/login");
    }
  });
};
</script>

<style scoped>
.register-wrapper {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #abb8c3 0%, #3d4a5d 100%);
}

.register-container {
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

.register-form {
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

.error-message {
  color: #e53e3e;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  font-weight: 500;
}

.register-btn {
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

.register-btn:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.85);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.register-btn:disabled {
  background: rgba(0, 0, 0, 0.4);
  cursor: not-allowed;
}

.login-link-container {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.95rem;
  color: #444;
}

.login-link {
  color: #111;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.5rem;
  transition: color 0.3s ease;
}

.login-link:hover {
  text-decoration: underline;
  color: #000;
}
</style>
