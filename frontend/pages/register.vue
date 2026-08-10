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
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { post } from "../utils/request";
import type { UserRegisterResponse } from "../types/user";

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
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-form {
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

.register-form:hover {
  transform: translateY(-5px) scale(1.01);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
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

.error-message {
  color: #ff4d4f;
  font-size: 0.85rem;
  margin-top: 0.3rem;
  padding: 0.3rem 0.5rem;
  background-color: rgba(255, 77, 79, 0.1);
  border-radius: 4px;
  border-left: 3px solid #ff4d4f;
  transition: all 0.3s ease;
}

.register-btn {
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

.register-btn::before {
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

.register-btn:hover:not(:disabled)::before {
  left: 0;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.register-btn:active:not(:disabled) {
  transform: translateY(0);
}

.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.login-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #666;
  font-size: 0.95rem;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
}

.login-link a::after {
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

.login-link a:hover {
  color: #764ba2;
}

.login-link a:hover::after {
  width: 100%;
}
</style>
