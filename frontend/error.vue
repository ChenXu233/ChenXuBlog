<template>
  <div class="error-page">
    <div class="error-inner">
      <span class="cx-eyebrow">ERROR / {{ error?.statusCode || 500 }}</span>
      <div class="error-code" aria-hidden="true">{{ error?.statusCode || 500 }}</div>
      <h1 class="error-title">{{ errorMessage }}</h1>
      <p class="error-sub">{{ errorSubtitle }}</p>
      <div class="error-actions">
        <NuxtLink to="/home" class="error-btn error-btn--primary">返回首页</NuxtLink>
        <button type="button" class="error-btn" @click="handleBack">返回上一页</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NuxtError } from "#app";

const props = defineProps<{ error: NuxtError }>();
const router = useRouter();

const errorMessage = computed(() => {
  switch (props.error?.statusCode) {
    case 404:
      return "页面不存在";
    case 403:
      return "没有访问权限";
    case 500:
      return "服务器出错了";
    default:
      return props.error?.message || "出错了";
  }
});

const errorSubtitle = computed(() => {
  switch (props.error?.statusCode) {
    case 404:
      return "你访问的页面可能已被移除或网址有误";
    case 403:
      return "你没有权限访问该页面，请联系管理员";
    case 500:
      return "服务器遇到了问题，请稍后重试";
    default:
      return "发生了一些意外情况";
  }
});

function handleBack() {
  if (window.history.length > 1) router.back();
  else router.push("/home");
}
</script>

<style scoped>
.error-page {
  min-height: 100dvh;
  display: grid;
  place-items: center;
  padding: 32px 20px;
  background: var(--cx-paper);
  color: var(--cx-ink);
}

.error-inner {
  position: relative;
  text-align: center;
}

.error-code {
  font-family: var(--cx-font-display);
  font-size: clamp(120px, 24vw, 320px);
  font-weight: 900;
  line-height: 0.78;
  letter-spacing: -0.08em;
  color: var(--cx-accent);
  user-select: none;
}

.error-title {
  position: relative;
  margin: -0.1em 0 0;
  font-family: var(--cx-font-display);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 800;
  letter-spacing: -0.03em;
}

.error-sub {
  margin: 14px 0 32px;
  font-size: 14px;
  color: var(--cx-ink-mute);
}

.error-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.error-btn {
  padding: 12px 22px;
  border-radius: 999px;
  border: 1px solid var(--cx-line-strong);
  background: transparent;
  color: var(--cx-ink);
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.1em;
  cursor: pointer;
}

.error-btn:hover {
  background: var(--cx-ink);
  color: var(--cx-paper);
}

.error-btn--primary {
  background: var(--cx-accent);
  border-color: var(--cx-accent);
  color: var(--cx-accent-ink);
}

.error-btn--primary:hover {
  background: color-mix(in srgb, var(--cx-accent) 85%, #000);
  color: var(--cx-accent-ink);
}
</style>
