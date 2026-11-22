<template>
  <div class="archive-page">
    <div class="cx-container">
      <header class="archive-hero">
        <span class="cx-eyebrow">ARCHIVE / 全部</span>
        <h1 class="archive-title">归档</h1>
        <p class="archive-sub">时间轴上铭刻的所有过往与踪迹。</p>
        <div class="archive-meta cx-mono">
          <span>{{ total }} POSTS</span>
          <span class="sep">/</span>
          <span
            >{{ groups.length }}
            {{ groups.length === 1 ? "YEAR" : "YEARS" }}</span
          >
        </div>
      </header>

      <div class="archive-grid">
        <aside class="year-rail" aria-label="年份">
          <a
            v-for="group in groups"
            :key="group.year"
            :href="`#year-${group.year}`"
            class="year-link"
          >
            <span>{{ group.year }}</span>
            <em class="cx-mono">{{
              String(group.items.length).padStart(2, "0")
            }}</em>
          </a>
        </aside>

        <section class="timeline">
          <div
            v-for="group in groups"
            :id="`year-${group.year}`"
            :key="group.year"
            class="year-group"
          >
            <header class="year-head">
              <h2 class="year-number">{{ group.year }}</h2>
              <span class="year-count cx-mono"
                >{{ group.items.length }} 篇</span
              >
            </header>

            <ol class="year-list">
              <li v-for="post in group.items" :key="post.id">
                <NuxtLink :to="`/article/${post.id}`" class="archive-row">
                  <time
                    class="row-date cx-mono"
                    :datetime="isoDate(post.created_at)"
                  >
                    {{ shortDate(post.created_at) }}
                  </time>
                  <span class="row-title">{{ post.title }}</span>
                  <span v-if="post.tags_name?.length" class="row-tag cx-mono">
                    {{ post.tags_name[0] }}
                  </span>
                  <span class="row-arrow" aria-hidden="true">→</span>
                </NuxtLink>
              </li>
            </ol>
          </div>

          <p v-if="!groups.length && !pending" class="archive-empty">
            暂无文章
          </p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type {
  BlogListResponse,
  BlogSummaryResponse,
} from "~/api-client/types.gen";
import { fetchAllPages } from "~/utils/pagination";

const { data, pending } = await useAsyncData<BlogListResponse>(
  "archive-list",
  () =>
    fetchAllPages<BlogSummaryResponse>((page, pageSize) =>
      useApiFetch<BlogListResponse>("/apis/v1/blog/", {
        query: { page, page_size: pageSize },
      }),
    ),
);

const blogs = computed<BlogSummaryResponse[]>(() => data.value?.items ?? []);
const total = computed(() => data.value?.total ?? 0);

const groups = computed(() => {
  const map = new Map<number, BlogSummaryResponse[]>();
  for (const post of blogs.value) {
    const year = new Date(post.created_at).getFullYear();
    if (!map.has(year)) map.set(year, []);
    map.get(year)!.push(post);
  }
  return [...map.entries()]
    .sort((a, b) => b[0] - a[0])
    .map(([year, items]) => ({ year, items }));
});

function isoDate(value: Date | string) {
  return new Date(value).toISOString();
}

function shortDate(value: Date | string) {
  const date = new Date(value);
  return `${String(date.getMonth() + 1).padStart(2, "0")}.${String(
    date.getDate(),
  ).padStart(2, "0")}`;
}

useSeo({
  title: "归档",
  description: "晨煦博客的全部文章归档，按时间排列。",
});
</script>

<style scoped>
.archive-page {
  padding-top: clamp(48px, 7vw, 96px);
}

.archive-hero {
  position: relative;
  padding-bottom: clamp(32px, 5vw, 56px);
  border-bottom: 1px solid var(--cx-line);
}

.archive-title {
  margin: 16px 0 0;
  font-family: var(--cx-font-display);
  font-size: clamp(64px, 12vw, 160px);
  font-weight: 900;
  letter-spacing: -0.06em;
  line-height: 0.82;
}

.archive-sub {
  margin: 24px 0 0;
  max-width: 40ch;
  font-size: 15px;
  line-height: 1.8;
  color: var(--cx-ink-soft);
}

.archive-meta {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  font-size: 10px;
  letter-spacing: 0.14em;
  color: var(--cx-ink-mute);
}

.sep {
  opacity: 0.4;
}

.archive-grid {
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  gap: clamp(32px, 5vw, 80px);
  padding-top: clamp(32px, 5vw, 56px);
}

.year-rail {
  position: sticky;
  top: 104px;
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.year-link {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 0;
  border-bottom: 1px solid var(--cx-line);
  font-family: var(--cx-font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--cx-ink-soft);
  transition: color 0.2s ease;
}

.year-link em {
  font-style: normal;
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--cx-ink-mute);
}

.year-link:hover {
  color: var(--cx-accent);
}

.year-group {
  padding-bottom: clamp(40px, 6vw, 72px);
  scroll-margin-top: 100px;
}

.year-head {
  display: flex;
  align-items: flex-end;
  gap: 18px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--cx-line-strong);
}

.year-number {
  margin: 0;
  font-family: var(--cx-font-display);
  font-size: clamp(48px, 7vw, 84px);
  font-weight: 800;
  letter-spacing: -0.05em;
  line-height: 0.85;
  color: var(--cx-accent);
}

.year-count {
  margin-bottom: 6px;
  padding: 5px 10px;
  border-radius: 999px;
  background: var(--cx-ink);
  color: var(--cx-paper);
  font-size: 10px;
  letter-spacing: 0.1em;
}

.year-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.archive-row {
  display: grid;
  grid-template-columns: 64px minmax(0, 1fr) auto 24px;
  align-items: baseline;
  gap: 18px;
  padding: 17px 4px;
  border-bottom: 1px solid var(--cx-line);
  transition:
    background 0.2s ease,
    padding 0.2s ease;
}

.archive-row:hover {
  background: color-mix(in srgb, var(--cx-accent) 5%, transparent);
  padding-left: 12px;
}

.row-date {
  font-size: 11px;
  letter-spacing: 0.06em;
  color: var(--cx-ink-mute);
}

.row-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  color: var(--cx-ink);
}

.row-tag {
  font-size: 10px;
  color: var(--cx-green);
}

.row-arrow {
  font-size: 14px;
  color: var(--cx-ink-mute);
  opacity: 0;
  transform: translateX(-4px);
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.archive-row:hover .row-arrow {
  opacity: 1;
  transform: none;
  color: var(--cx-accent);
}

.archive-empty {
  padding: 48px 0;
  color: var(--cx-ink-mute);
}

@media (max-width: 860px) {
  .archive-grid {
    grid-template-columns: 1fr;
  }

  .year-rail {
    display: none;
  }

  .archive-row {
    grid-template-columns: 52px minmax(0, 1fr) 20px;
    gap: 12px;
  }

  .row-tag {
    display: none;
  }
}
</style>
