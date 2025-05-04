<template>
  <div
    class="bg-cover bg-center w-full h-screen"
    style="background-image: url(&quot;http://www.98qy.com/sjbz/api.php&quot;)"
  >
    <AppBar />
    <main class="max-w-6xl mx-auto px-4 py-8">
      <div class="grid md:grid-cols-3 gap-8">
        <article
          v-for="post in articles"
          :key="post.id"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow"
        >
          <img
            v-if="post.cover"
            :src="post.cover"
            class="w-full h-48 object-cover"
          />
          <div class="p-6">
            <div class="flex items-center space-x-2 text-sm text-gray-500">
              <span>{{ formatDate(post.date) }}</span>
              <span>•</span>
              <div class="flex space-x-2">
                <span
                  v-for="tag in post.tags"
                  class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <h2 class="mt-4 text-2xl font-semibold text-gray-800">
              {{ post.title }}
            </h2>
            <p class="mt-2 text-gray-600 line-clamp-3">
              {{ post.content }}
            </p>
            <button
              @click="viewDetail()"
              class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              阅读更多
            </button>
          </div>
        </article>
      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import type { Article } from "./types/article";
import AppBar from "./components/AppBar.vue";
import { useRouter } from "vue-router";

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
  const $r = useRouter();
  $r.push("/home");
};

onMounted(() => {
  console.log("你好，欢迎来到我的博客");
});
</script>
