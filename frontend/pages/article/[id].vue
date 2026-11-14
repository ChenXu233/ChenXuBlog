<template>
  <article v-if="article" class="article-detail">
    <div class="reading-progress" aria-hidden="true">
      <span :style="{ transform: `scaleX(${progress})` }" />
    </div>

    <header class="article-hero">
      <div class="cx-container hero-inner">
        <div class="hero-top cx-mono">
          <NuxtLink to="/article" class="back-link">← 文章</NuxtLink>
          <span class="sep">/</span>
          <time :datetime="isoDate(article.created_at)">
            {{ formatDate(article.created_at) }}
          </time>
          <span class="sep">/</span>
          <span>{{ readingTime }} MIN READ</span>
          <span class="sep">/</span>
          <span>{{ article.view_count }} VIEWS</span>
        </div>

        <div class="hero-rule" aria-hidden="true" />

        <h1 class="article-title">{{ article.title }}</h1>

        <div class="hero-bottom">
          <ul v-if="article.tags_name?.length" class="tags">
            <li v-for="tag in article.tags_name" :key="tag" class="cx-chip">
              {{ tag }}
            </li>
          </ul>

          <div class="hero-actions">
            <button
              type="button"
              class="like-btn"
              :class="{ liked: hasLiked }"
              @click="handleLike"
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path
                  d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 22l7.8-8.6 1-1a5.5 5.5 0 0 0 0-7.8z"
                />
              </svg>
              <span>{{ likesCount }}</span>
            </button>
            <NuxtLink v-if="canEdit" :to="`/article/edit/${article.id}`" class="edit-link">
              编辑
            </NuxtLink>
          </div>
        </div>
      </div>
    </header>

    <div v-if="article.cover_url" class="cover-wrap cx-container">
      <img
        :src="article.cover_url"
        :alt="article.title"
        class="cover"
        loading="eager"
        decoding="async"
      />
    </div>

    <div class="article-grid cx-container">
      <div class="body-col">
        <details v-if="toc.length > 1" class="toc-mobile">
          <summary>目录 / CONTENTS</summary>
          <ol>
            <li v-for="item in toc" :key="item.id">
              <a :href="`#${item.id}`">{{ item.title }}</a>
            </li>
          </ol>
        </details>

        <div class="cx-prose" v-html="html" />

        <div class="article-end">
          <span class="end-mark cx-mono">END</span>
          <div class="end-rule" />
          <NuxtLink to="/article" class="end-link">返回文章列表 →</NuxtLink>
        </div>
      </div>

      <aside v-if="toc.length > 1" class="toc-desktop" aria-label="文章目录">
        <div class="toc-inner">
          <span class="cx-eyebrow">目录 / CONTENTS</span>
          <a
            v-for="item in toc"
            :key="item.id"
            :href="`#${item.id}`"
            class="toc-link"
            :class="{ active: activeId === item.id }"
            :style="{ paddingLeft: `${(item.level - minTocLevel) * 12}px` }"
          >
            {{ item.title }}
          </a>
        </div>
      </aside>
    </div>

    <div class="comments-outer cx-container">
      <section class="comments-wrap">
        <div class="comments-head">
          <h2>评论</h2>
          <span class="cx-eyebrow">DISCUSSION</span>
        </div>
        <CommentList :blog-id="article.id" />
      </section>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { BlogResponse } from "~/api-client/types.gen";
import { blogService } from "~/service/blog";

const route = useRoute();
const auth = useAuthStore();
const id = Number(route.params.id);

const { data: article } = await useAsyncData<BlogResponse>(
  `article-${id}`,
  () => useApiFetch<BlogResponse>(`/apis/v1/blog/${id}`),
);

if (!article.value) {
  throw createError({ statusCode: 404, statusMessage: "文章不存在" });
}

const rendered = computed(() => renderMarkdown(article.value?.body || ""));
const html = computed(() => rendered.value.html);
const toc = computed(() => rendered.value.toc);
const minTocLevel = computed(() =>
  toc.value.length ? Math.min(...toc.value.map((item) => item.level)) : 2,
);

const plainText = computed(() =>
  (article.value?.body || "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/<[^>]+>/g, " ")
    .replace(/[#>*_`~-]/g, " ")
    .replace(/\s+/g, " ")
    .trim(),
);

const description = computed(() => {
  const text = plainText.value;
  return text.length > 140 ? text.slice(0, 140) + "…" : text;
});

const readingTime = computed(() =>
  Math.max(1, Math.round(plainText.value.length / 400)),
);

const likesCount = ref(article.value?.likes_count ?? 0);
const hasLiked = ref(false);
const canEdit = computed(
  () =>
    auth.isAuthenticated &&
    !!article.value &&
    article.value.user_uuid === auth.user?.uuid,
);

const progress = ref(0);
const activeId = ref("");

function isoDate(value: Date | string) {
  return new Date(value).toISOString();
}

function formatDate(value: Date | string) {
  const date = new Date(value);
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, "0")}.${String(date.getDate()).padStart(2, "0")}`;
}

function onScroll() {
  const doc = document.documentElement;
  const max = doc.scrollHeight - window.innerHeight;
  progress.value = max > 0 ? Math.min(1, window.scrollY / max) : 0;

  let current = toc.value[0]?.id ?? "";
  for (const item of toc.value) {
    const el = document.getElementById(item.id);
    if (el && el.getBoundingClientRect().top <= 120) current = item.id;
  }
  activeId.value = current;
}

onMounted(() => {
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", onScroll);
  window.removeEventListener("resize", onScroll);
});

async function handleLike() {
  if (!article.value) return;
  if (!auth.isAuthenticated) {
    await navigateTo("/login");
    return;
  }

  const next = !hasLiked.value;
  hasLiked.value = next;
  likesCount.value = Math.max(0, likesCount.value + (next ? 1 : -1));

  try {
    await blogService.likeBlog(article.value.id);
  } catch {
    hasLiked.value = !next;
    likesCount.value = Math.max(0, likesCount.value + (next ? -1 : 1));
  }
}

if (article.value) {
  const siteUrl = String(useRuntimeConfig().public.siteUrl || "").replace(/\/$/, "");
  useSeo({
    title: article.value.title,
    description: description.value,
    image: article.value.cover_url || undefined,
    type: "article",
    publishedTime: article.value.created_at,
    modifiedTime: article.value.updated_at,
    tags: article.value.tags_name,
    author: "晨煦",
    jsonLd: {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      headline: article.value.title,
      description: description.value,
      datePublished: new Date(article.value.created_at).toISOString(),
      dateModified: new Date(article.value.updated_at).toISOString(),
      author: {
        "@type": "Person",
        name: "晨煦",
        url: siteUrl + "/home",
      },
      mainEntityOfPage: `${siteUrl}/article/${article.value.id}`,
      ...(article.value.cover_url
        ? {
            image: article.value.cover_url.startsWith("http")
              ? article.value.cover_url
              : siteUrl + article.value.cover_url,
          }
        : {}),
      keywords: (article.value.tags_name || []).join(", "),
    },
  });
}
</script>

<style scoped>
.article-detail {
  padding-bottom: 40px;
}

.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 90;
  height: 2px;
  background: transparent;
  pointer-events: none;
}

.reading-progress span {
  display: block;
  height: 100%;
  background: var(--cx-accent);
  transform-origin: left;
  transform: scaleX(0);
  will-change: transform;
}

.article-hero {
  position: relative;
  padding: clamp(48px, 7vw, 88px) 0 clamp(28px, 4vw, 44px);
  overflow: clip;
  border-bottom: 1px solid var(--cx-line);
}

.hero-inner {
  position: relative;
  z-index: 1;
}

.hero-top {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--cx-ink-mute);
  text-transform: uppercase;
}

.back-link {
  color: var(--cx-ink-soft);
  transition: color 0.2s ease;
}

.back-link:hover {
  color: var(--cx-accent);
}

.sep {
  opacity: 0.4;
}

.hero-rule {
  width: 56px;
  height: 4px;
  margin-top: clamp(22px, 3vw, 34px);
  background: var(--cx-accent);
}

.article-title {
  margin: clamp(18px, 2.4vw, 28px) 0 0;
  max-width: 20ch;
  font-family: var(--cx-font-display);
  font-size: clamp(38px, 6.4vw, 82px);
  font-weight: 800;
  letter-spacing: -0.045em;
  line-height: 1.06;
  color: var(--cx-ink);
  text-wrap: balance;
}

.hero-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-top: clamp(22px, 3vw, 34px);
}

.tags {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0;
  padding: 0;
}

.tags .cx-chip:nth-child(3n + 1) {
  background: var(--cx-accent);
  border-color: var(--cx-accent);
  color: var(--cx-accent-ink);
}

.tags .cx-chip:nth-child(3n + 2) {
  background: var(--cx-blue);
  border-color: var(--cx-blue);
  color: var(--cx-blue-ink);
}

.tags .cx-chip:nth-child(3n + 3) {
  background: var(--cx-lime);
  border-color: var(--cx-lime);
  color: var(--cx-lime-ink);
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 16px;
  border-radius: 999px;
  border: 1px solid var(--cx-line-strong);
  background: transparent;
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease;
}

.like-btn:hover,
.like-btn.liked {
  background: var(--cx-accent);
  border-color: var(--cx-accent);
  color: var(--cx-accent-ink);
}

.edit-link {
  padding: 9px 4px;
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  color: var(--cx-ink-soft);
  text-decoration: underline;
  text-underline-offset: 4px;
}

.cover-wrap {
  margin-top: clamp(24px, 4vw, 44px);
}

.cover {
  width: 100%;
  max-height: 520px;
  object-fit: cover;
  border-radius: 2px;
  border: 1px solid var(--cx-line);
}

.article-grid {
  display: grid;
  grid-template-columns: minmax(0, 720px) 200px;
  justify-content: center;
  gap: clamp(40px, 6vw, 96px);
  padding-top: clamp(32px, 5vw, 56px);
}

.body-col {
  min-width: 0;
}

.toc-desktop {
  align-self: start;
  position: sticky;
  top: 104px;
}

.toc-inner {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 8px;
  border-top: 1px solid var(--cx-line);
}

.toc-link {
  display: block;
  padding-top: 2px;
  padding-bottom: 2px;
  font-size: 12px;
  line-height: 1.5;
  color: var(--cx-ink-mute);
  transition: color 0.2s ease;
}

.toc-link:hover,
.toc-link.active {
  color: var(--cx-accent);
}

.toc-mobile {
  display: none;
  margin-bottom: 28px;
  border: 1px solid var(--cx-line);
  border-radius: var(--cx-radius-sm);
  padding: 14px 16px;
  background: linear-gradient(
    145deg,
    rgba(var(--cx-glass-a), 0.95),
    rgba(var(--cx-glass-b), 0.93)
  );
}

.toc-mobile summary {
  cursor: pointer;
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.12em;
  color: var(--cx-ink-soft);
}

.toc-mobile ol {
  margin: 14px 0 0;
  padding-left: 18px;
  font-size: 13px;
  line-height: 1.9;
}

.toc-mobile a {
  color: var(--cx-ink-soft);
}

.article-end {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-top: 56px;
  padding-top: 22px;
  border-top: 1px solid var(--cx-line);
}

.end-mark {
  font-size: 10px;
  letter-spacing: 0.2em;
  color: var(--cx-accent);
}

.end-rule {
  flex: 1;
  height: 1px;
  background: var(--cx-line);
}

.end-link {
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  color: var(--cx-ink-soft);
}

.end-link:hover {
  color: var(--cx-accent);
}

.comments-outer {
  display: grid;
  grid-template-columns: minmax(0, 720px) 200px;
  justify-content: center;
  gap: clamp(40px, 6vw, 96px);
  margin-top: clamp(56px, 8vw, 96px);
}

.comments-wrap {
  grid-column: 1;
}

.comments-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--cx-line);
  margin-bottom: 28px;
}

.comments-head h2 {
  margin: 0;
  font-family: var(--cx-font-display);
  font-size: clamp(24px, 3vw, 34px);
  font-weight: 800;
  letter-spacing: -0.03em;
}

@media (max-width: 1080px) {
  .article-grid {
    grid-template-columns: minmax(0, 720px);
  }

  .toc-desktop {
    display: none;
  }

  .toc-mobile {
    display: block;
  }
}

@media (max-width: 640px) {
  .hero-bottom {
    flex-direction: column;
    align-items: flex-start;
  }

  .article-title {
    max-width: none;
  }

  .comments-outer {
    grid-template-columns: minmax(0, 720px);
    margin-top: 56px;
  }
}
</style>
