<template>
  <div class="archive-page">
    <section class="archive-section">
      <h1>归档</h1>
      <p>时间轴上铭刻的所有过往与踪迹。</p>

      <div v-if="loading" class="archive-loading">加载中...</div>
      <p v-else-if="!groups.length" class="archive-empty">暂无文章</p>

      <div v-for="group in groups" :key="group.year" class="year-group">
        <h2 class="year">
          {{ group.year }}<span>{{ group.items.length }} 篇</span>
        </h2>
        <ul class="timeline">
          <li v-for="b in group.items" :key="b.id">
            <NuxtLink :to="`/article/${b.id}`">
              <span class="dot"></span>
              <span class="date">{{ shortDate(b.created_at) }}</span>
              <span class="title">{{ b.title }}</span>
            </NuxtLink>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { blogService } from "../service/blog";
import type { BlogResponse } from "../src/client/types.gen";

const blogs = ref<BlogResponse[]>([]);
const loading = ref(true);

// ponytail: 单次拉 100 篇按年分组；文章超百篇再改后端归档接口
const groups = computed(() => {
  const map = new Map<number, BlogResponse[]>();
  for (const b of blogs.value) {
    const year = new Date(b.created_at).getFullYear();
    if (!map.has(year)) map.set(year, []);
    map.get(year)!.push(b);
  }
  return [...map.entries()]
    .sort((a, b) => b[0] - a[0])
    .map(([year, items]) => ({ year, items }));
});

const shortDate = (d: Date | number | string) => {
  const t = new Date(d);
  return `${String(t.getMonth() + 1).padStart(2, "0")}-${String(
    t.getDate(),
  ).padStart(2, "0")}`;
};

onMounted(async () => {
  try {
    const data = await blogService.getBlogList({ page: 1, page_size: 100 });
    blogs.value = data.items;
  } catch (e) {
    console.error("加载归档失败:", e);
  } finally {
    loading.value = false;
  }
});

useSeo({ title: "归档", description: "所有文章的时间线" });
</script>

<style scoped>
.archive-page {
  color: #fff;
  font-family: "JetBrains Mono", monospace;
  overflow-x: clip;
  cursor: none;
  min-height: 100vh;
}

.archive-section {
  padding: 8rem 10vw;
  max-width: 900px;
  margin: 0 auto;
}

.archive-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center;
}

.archive-section > p,
.archive-empty,
.archive-loading {
  color: #aaa;
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: 3rem;
}

.year-group {
  margin-bottom: 3rem;
}

.year {
  font-size: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  padding-bottom: 0.5rem;
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.year span {
  font-size: 1rem;
  color: #888;
}

.timeline {
  list-style: none;
  padding: 0.5rem 0 0 0.75rem;
  border-left: 1px solid rgba(255, 255, 255, 0.15);
}

.timeline li a {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  padding: 0.6rem 0;
  color: #ccc;
  text-decoration: none;
  position: relative;
  transition: color 0.2s;
}

.timeline li a:hover .title {
  color: #fff;
}

.dot {
  position: absolute;
  left: -1rem;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  transition: background 0.2s;
}

.timeline li a:hover .dot {
  background: #fff;
}

.date {
  flex-shrink: 0;
  color: #888;
  font-size: 0.9rem;
  width: 3.5em;
}
</style>
