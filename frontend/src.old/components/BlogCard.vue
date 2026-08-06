<template>
  <article
    class="glass-panel group relative overflow-hidden cursor-pointer blog-card flex flex-col md:flex-row h-full md:h-64"
    @click="goToDetail"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
    ref="cardRef"
    :style="{
      transform: `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
    }"
  >
    <div class="h-48 md:h-full md:w-1/3 flex-shrink-0 overflow-hidden relative">
      <img
        v-if="article.cover_url"
        :src="article.cover_url"
        :alt="article.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105 filter sepia-[0.3] contrast-[0.9] group-hover:sepia-0 group-hover:contrast-100"
      />
      <div
        v-else
        class="w-full h-full bg-primary/10 flex items-center justify-center"
      >
        <i class="fa fa-image text-4xl text-primary/30"></i>
      </div>
      <div
        class="absolute inset-0 bg-gradient-to-t md:bg-gradient-to-r from-bg/80 to-transparent pointer-events-none"
      ></div>
    </div>
    <div class="p-6 md:p-8 flex flex-col flex-1">
      <div class="flex items-center gap-2 mb-3 flex-wrap">
        <span
          v-for="tag in article.tags_name"
          :key="tag"
          class="px-2 py-1 text-[10px] uppercase tracking-widest font-mono rounded bg-primary/10 text-primary border border-primary/20"
        >
          {{ tag }}
        </span>
      </div>
      <h3
        class="text-xl font-bold mb-3 text-text group-hover:text-primary transition-colors line-clamp-2"
      >
        {{ article.title }}
      </h3>
      <p class="text-text-light text-sm line-clamp-3 mb-4 flex-1">
        {{ excerpt }}
      </p>
      <div
        class="flex items-center text-xs text-text-light font-mono gap-4 uppercase tracking-wider"
      >
        <span class="flex items-center gap-1.5">
          <i class="fa fa-calendar-o opacity-70"></i>
          {{ formatDate(article.created_at) }}
        </span>
        <span class="flex items-center gap-1.5 ml-auto">
          <i class="fa fa-eye opacity-70"></i>
          {{ article.view_count }}
        </span>
        <span class="flex items-center gap-1.5">
          <i class="fa fa-heart-o opacity-70"></i>
          {{ article.like }}
        </span>
      </div>
    </div>

    <!-- 3D 光泽反射层 -->
    <div
      class="pointer-events-none absolute inset-0 z-10 transition-opacity duration-300 opacity-0 group-hover:opacity-100"
      :style="{
        background: `radial-gradient(circle at ${mouseX}px ${mouseY}px, rgba(255,255,255,0.4) 0%, transparent 60%)`,
        mixBlendMode: 'overlay',
      }"
    ></div>
  </article>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import type { Article } from "../types/article";

const props = defineProps<{
  article: Article;
}>();

const router = useRouter();

const excerpt = computed(() => {
  const text = props.article.body.replace(/[#*`\[\]]/g, "").trim();
  return text.length > 120 ? text.substring(0, 120) + "..." : text;
});

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

const goToDetail = () => {
  router.push(`/article/${props.article.id}`);
};

// 3D Tilt Effect
const cardRef = ref<HTMLElement | null>(null);
const rotateX = ref(0);
const rotateY = ref(0);
const mouseX = ref(0);
const mouseY = ref(0);

const handleMouseMove = (e: MouseEvent) => {
  if (!cardRef.value) return;
  const rect = cardRef.value.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  mouseX.value = x;
  mouseY.value = y;

  const centerX = rect.width / 2;
  const centerY = rect.height / 2;

  // 阻尼系数越小倾斜越大
  rotateY.value = ((x - centerX) / centerX) * 5;
  rotateX.value = -((y - centerY) / centerY) * 5;
};

const handleMouseLeave = () => {
  rotateX.value = 0;
  rotateY.value = 0;
};
</script>

<style scoped>
.blog-card {
  transition:
    transform 0.3s cubic-bezier(0.23, 1, 0.32, 1),
    box-shadow 0.3s ease;
}
.blog-card:hover {
  box-shadow: var(--shadow-glow), var(--shadow-soft);
  border-color: rgba(255, 255, 255, 0.4);
}
</style>
