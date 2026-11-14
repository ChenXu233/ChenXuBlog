<template>
  <article class="blog-card cx-glass" @click="goToDetail">
    <div v-if="article.cover_url" class="card-cover">
      <img :src="article.cover_url" :alt="article.title" loading="lazy" decoding="async" />
    </div>
    <div class="card-body">
      <div class="card-top">
        <time class="card-date cx-mono" :datetime="isoDate(article.created_at)">
          {{ formatDate(article.created_at) }}
        </time>
        <span class="card-views cx-mono">{{ article.view_count }} views</span>
      </div>
      <h3 class="card-title">{{ article.title }}</h3>
      <p class="card-excerpt">{{ excerpt }}</p>
      <ul v-if="article.tags_name?.length" class="card-tags">
        <li v-for="tag in article.tags_name" :key="tag" class="card-tag">
          {{ tag }}
        </li>
      </ul>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { BlogResponse } from "~/api-client/types.gen";

const props = defineProps<{
  article: BlogResponse;
}>();

const router = useRouter();

const excerpt = computed(() => {
  const text = props.article.body
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/<[^>]+>/g, " ")
    .replace(/[#>*_`~-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return text.length > 110 ? text.slice(0, 110) + "…" : text;
});

function isoDate(value: Date | string) {
  return new Date(value).toISOString();
}

function formatDate(value: Date | string) {
  const date = new Date(value);
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, "0")}.${String(date.getDate()).padStart(2, "0")}`;
}

function goToDetail() {
  router.push(`/article/${props.article.id}`);
}
</script>

<style scoped>
.blog-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: var(--cx-radius);
  cursor: pointer;
  transition:
    transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1),
    border-color 0.3s ease;
}

.blog-card:hover {
  transform: translateY(-3px);
  border-color: var(--cx-accent);
}

.card-cover {
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border-bottom: 1px solid var(--cx-line);
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.blog-card:hover .card-cover img {
  transform: scale(1.04);
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 10px;
  letter-spacing: 0.08em;
  color: var(--cx-ink-mute);
}

.card-title {
  margin: 0;
  font-family: var(--cx-font-display);
  font-size: 19px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.35;
  color: var(--cx-ink);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-excerpt {
  margin: 0;
  font-size: 13px;
  line-height: 1.75;
  color: var(--cx-ink-soft);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  list-style: none;
  margin: 6px 0 0;
  padding: 0;
}

.card-tag {
  font-family: var(--cx-font-mono);
  font-size: 10px;
  letter-spacing: 0.06em;
  color: var(--cx-green);
}

.card-tag::before {
  content: "#";
  margin-right: 2px;
  opacity: 0.6;
}
</style>
