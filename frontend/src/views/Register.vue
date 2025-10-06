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
        <a href="/login">立即登录</a>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { request } from "../utils/request";

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

  isSubmitting.value = true;

  request({
    url: "/register",
    method: "POST",
    data: form,
  })
    .then((res) => {
      if (res.code === 200) {
        // 注册成功后跳转到登录页面
        router.push("/login");
      }
    })
    .catch((err) => {
      console.error("注册失败:", err);
      // 可以在这里显示更友好的错误提示
    })
    .finally(() => {
      isSubmitting.value = false;
    });
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.register-form {
  background: white;
  padding: 2rem 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.nav-brand {
  display: inline-block;
  margin-bottom: 1rem;
  color: #1890ff;
  text-decoration: none;
  font-size: 0.9rem;
}

.nav-brand:hover {
  text-decoration: underline;
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
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.error-message {
  color: #ff4d4f;
  font-size: 0.8rem;
  margin-top: 0.3rem;
}

.register-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.register-btn:hover:not(:disabled) {
  background-color: #40a9ff;
}

.register-btn:disabled {
  background-color: #d9d9d9;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.login-link a {
  color: #1890ff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
