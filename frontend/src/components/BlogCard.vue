<template>
  <article class="blog-card" @click="goToDetail">
    <div class="card-cover" v-if="article.cover_url">
      <img :src="article.cover_url" :alt="article.title" />
    </div>
    <div class="card-content">
      <div class="card-tags" v-if="article.tags_name?.length">
        <span v-for="tag in article.tags_name" :key="tag" class="tag">{{ tag }}</span>
      </div>
      <h3 class="card-title">{{ article.title }}</h3>
      <p class="card-excerpt">{{ excerpt }}</p>
      <div class="card-meta">
        <span class="meta-item">
          <i class="fa fa-calendar"></i>
          {{ formatDate(article.created_at) }}
        </span>
        <span class="meta-item">
          <i class="fa fa-eye"></i>
          {{ article.view_count }}
        </span>
        <span class="meta-item">
          <i class="fa fa-heart"></i>
          {{ article.like }}
        </span>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from "vue";
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
</script>

<style scoped>
.blog-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.blog-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-cover {
  height: 160px;
  overflow: hidden;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.blog-card:hover .card-cover img {
  transform: scale(1.05);
}

.card-content {
  padding: 16px;
}

.card-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 12px;
  border-radius: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-excerpt {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #999;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
