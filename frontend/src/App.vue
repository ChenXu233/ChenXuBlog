<template>
  <div
    class="bg-cover bg-center w-full min-h-screen relative"
    style="background-image: url(&quot;http://www.98qy.com/sjbz/api.php&quot;)"
  >
    <!-- 高斯模糊背景层 -->
    <div
      :style="{ backdropFilter: `blur(${blurStrength}px)` }"
      class="absolute inset-0 bg-opacity-50"
    ></div>

    <!-- 内容层 -->
    <div class="relative z-10">
      <AppBar />

      <!-- 新增个人信息区域 -->
      <div
        class="flex flex-col items-center justify-center min-h-screen pt-16 pb-24"
      >
        <div class="avatar-container relative mb-6">
          <div class="w-32 h-32 rounded-full bg-white p-1 animate-pulse">
            <img
              src="http://q.qlogo.cn/headimg_dl?dst_uin=1964324406&spec=640&img_type=jpg"
              alt="头像"
              class="w-full h-full rounded-full object-cover"
            />
          </div>
          <!-- 头像动画效果 -->
          <div
            class="absolute -inset-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full blur opacity-30 animate-spin"
          ></div>
        </div>
        <h1 class="text-4xl font-bold text-white mb-2">ChenXu's Blog</h1>
        <p class="text-xl text-white/80 mb-8">ChenXu</p>
        <div class="animate-bounce">
          <svg
            class="w-8 h-8 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            ></path>
          </svg>
        </div>
      </div>

      <!-- 博客文章区域 -->
      <main class="max-w-6xl mx-auto px-4 py-16">
        <div class="grid md:grid-cols-3 gap-8">// ... existing code ...</div>
      </main>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted } from "vue";
import type { Article } from "./types/article";
import AppBar from "./components/AppBar.vue";
import router from "./router";

const articles = ref<Article[]>([
  {
    id: 1,
    title: "Tailwind CSS实践指南",
    content: "详细介绍如何在Vue项目中集成Tailwind CSS...",
    date: "2024-04-26",
    tags: ["前端", "CSS"],
    cover: "/cover1.jpg",
  },
]);

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};

const viewDetail = () => {
  router.push({ path: "/article" });
};

// 模糊强度，默认为8px
const blurStrength = ref(8);

onMounted(() => {
  console.log("你好，欢迎来到我的博客");
});
</script>

<style scoped>
.avatar-container {
  position: relative;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 4s linear infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>
