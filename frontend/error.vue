<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800"
  >
    <div class="text-center px-4">
      <div
        class="text-8xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-rose-400 to-amber-400"
      >
        {{ error?.statusCode || 500 }}
      </div>
      <h1 class="text-2xl font-semibold mb-2 text-white">
        {{ errorMessage }}
      </h1>
      <p class="text-gray-400 mb-8">{{ errorSubtitle }}</p>
      <div class="flex justify-center gap-3">
        <UButton icon="i-heroicons-home" color="primary" to="/home"
          >返回首页</UButton
        >
        <UButton
          variant="ghost"
          icon="i-heroicons-arrow-uturn-left"
          @click="handleBack"
        >
          返回上一页
        </UButton>
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
  if (window.history.length > 1) {
    router.back();
  } else {
    router.push("/home");
  }
}
</script>
