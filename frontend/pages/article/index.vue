<template>
  <div class="article-page">
    <div class="cx-container">
      <header class="page-hero">
        <div class="hero-main">
          <span class="cx-eyebrow">INDEX / 文章</span>
          <h1 class="hero-title">文章</h1>
        </div>
        <div class="hero-count">
          <span class="count-value">{{ total }}</span>
          <span class="count-label">篇公开文章</span>
        </div>
      </header>

      <div class="article-layout">
        <aside class="rail">
          <div class="rail-block">
            <label class="rail-label cx-eyebrow" for="article-search">
              搜索 / SEARCH
            </label>
            <form class="search" role="search" @submit.prevent="applySearch">
              <input
                id="article-search"
                v-model="draftSearch"
                type="search"
                class="search-input"
                placeholder="标题或正文…"
                autocomplete="off"
              />
              <button type="submit" class="search-submit" aria-label="搜索">
                <svg
                  width="15"
                  height="15"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  aria-hidden="true"
                >
                  <circle cx="11" cy="11" r="7" />
                  <path d="M20 20l-3.5-3.5" />
                </svg>
              </button>
            </form>
            <button
              v-if="search"
              type="button"
              class="clear-search cx-mono"
              @click="clearSearch"
            >
              × 清除「{{ search }}」
            </button>
          </div>

          <div v-if="tagOptions.length" class="rail-block">
            <span class="rail-label cx-eyebrow">标签 / TAGS</span>
            <div class="tag-filter">
              <button
                type="button"
                class="cx-chip"
                :class="{ 'cx-chip--accent': !tag }"
                @click="setTag('')"
              >
                全部
              </button>
              <button
                v-for="name in tagOptions"
                :key="name"
                type="button"
                class="cx-chip"
                :class="{ 'cx-chip--accent': tag === name }"
                @click="setTag(name)"
              >
                {{ name }}
              </button>
            </div>
          </div>

          <div class="rail-block rail-meta">
            <span class="cx-eyebrow">RSS</span>
            <a href="/rss.xml" target="_blank" rel="noopener" class="rail-link">
              订阅文章更新 ↗
            </a>
          </div>
        </aside>

        <section class="list-area" :aria-busy="pending">
          <div v-if="items.length" class="list-panel cx-glass">
            <NuxtLink
              v-for="(post, index) in items"
              :key="post.id"
              :to="`/article/${post.id}`"
              class="post-row"
              :class="{ 'is-featured': isFeatured(index) }"
            >
              <span class="row-index cx-mono">
                {{ String((page - 1) * pageSize + index + 1).padStart(2, "0") }}
              </span>

              <div class="row-main">
                <div v-if="post.tags_name?.length" class="row-tags">
                  <span
                    v-for="name in post.tags_name"
                    :key="name"
                    class="row-tag"
                  >
                    {{ name }}
                  </span>
                </div>
                <h2 class="row-title">{{ post.title }}</h2>
                <p class="row-excerpt">{{ post.excerpt }}</p>
              </div>

              <div class="row-meta">
                <time :datetime="isoDate(post.created_at)">
                  {{ formatDate(post.created_at) }}
                </time>
                <span class="row-views cx-mono"
                  >{{ post.view_count }} views</span
                >
              </div>
            </NuxtLink>
          </div>

          <div v-else-if="!pending" class="empty-state cx-glass">
            <p class="empty-title">没有找到文章</p>
            <p class="empty-desc">换个关键词，或者看看全部文章。</p>
            <button type="button" class="empty-btn" @click="resetAll">
              重置筛选
            </button>
          </div>

          <div v-else class="loading-state" aria-hidden="true">
            <span v-for="i in 4" :key="i" class="loading-row" />
          </div>

          <nav v-if="totalPages > 1" class="pager" aria-label="分页">
            <button
              type="button"
              class="pager-btn"
              :disabled="page <= 1"
              @click="goToPage(page - 1)"
            >
              ←
            </button>
            <span class="pager-status cx-mono">
              {{ String(page).padStart(2, "0") }} /
              {{ String(totalPages).padStart(2, "0") }}
            </span>
            <button
              type="button"
              class="pager-btn"
              :disabled="page >= totalPages"
              @click="goToPage(page + 1)"
            >
              →
            </button>
          </nav>
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

const route = useRoute();
const router = useRouter();

const pageSize = 10;
const page = ref(Math.max(1, Number(route.query.page) || 1));
const search = ref(String(route.query.q || ""));
const tag = ref(String(route.query.tag || ""));
const draftSearch = ref(search.value);

const { data, pending } = await useAsyncData<BlogListResponse>(
  "article-list",
  () =>
    useApiFetch<BlogListResponse>("/apis/v1/blog/", {
      query: {
        page: page.value,
        page_size: pageSize,
        search: search.value || undefined,
        tag: tag.value || undefined,
      },
    }),
  { watch: [page, search, tag] },
);

const items = computed<BlogSummaryResponse[]>(() => data.value?.items ?? []);
const total = computed(() => data.value?.total ?? 0);
const totalPages = computed(() => data.value?.total_pages ?? 1);

const tagOptions = computed(() => {
  const set = new Set<string>();
  for (const post of items.value) {
    for (const name of post.tags_name ?? []) set.add(name);
  }
  return [...set].slice(0, 8);
});

function isFeatured(index: number) {
  return page.value === 1 && index === 0 && !search.value && !tag.value;
}

function isoDate(value: Date | string) {
  return new Date(value).toISOString();
}

function formatDate(value: Date | string) {
  const date = new Date(value);
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(
    2,
    "0",
  )}.${String(date.getDate()).padStart(2, "0")}`;
}

function syncQuery() {
  const query: Record<string, string> = {};
  if (page.value > 1) query.page = String(page.value);
  if (search.value) query.q = search.value;
  if (tag.value) query.tag = tag.value;
  router.replace({ query });
}

function applySearch() {
  search.value = draftSearch.value.trim();
  page.value = 1;
  syncQuery();
}

function clearSearch() {
  draftSearch.value = "";
  search.value = "";
  page.value = 1;
  syncQuery();
}

function setTag(name: string) {
  tag.value = name;
  page.value = 1;
  syncQuery();
}

function goToPage(next: number) {
  if (next < 1 || next > totalPages.value) return;
  page.value = next;
  syncQuery();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetAll() {
  draftSearch.value = "";
  search.value = "";
  tag.value = "";
  page.value = 1;
  syncQuery();
}

watch(
  () => route.query,
  (query) => {
    const nextPage = Math.max(1, Number(query.page) || 1);
    const nextSearch = String(query.q || "");
    const nextTag = String(query.tag || "");
    if (nextPage !== page.value) page.value = nextPage;
    if (nextSearch !== search.value) {
      search.value = nextSearch;
      draftSearch.value = nextSearch;
    }
    if (nextTag !== tag.value) tag.value = nextTag;
  },
);

useSeo({
  title: "文章",
  description: "晨煦的所有文章索引：代码、物理、哲学与生活。",
});
</script>

<style scoped>
.article-page {
  padding-top: clamp(48px, 7vw, 96px);
}

.page-hero {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 32px;
  padding-bottom: clamp(32px, 5vw, 56px);
  border-bottom: 1px solid var(--cx-line);
}

.hero-main {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.hero-title {
  margin: 0;
  font-family: var(--cx-font-display);
  font-size: clamp(64px, 12vw, 160px);
  font-weight: 900;
  letter-spacing: -0.06em;
  line-height: 0.82;
  color: var(--cx-ink);
}

.hero-count {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  padding: 16px 20px;
  border-radius: 18px;
  background: var(--cx-accent);
  color: var(--cx-accent-ink);
  flex-shrink: 0;
}

.count-value {
  font-family: var(--cx-font-display);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 800;
  line-height: 1;
}

.count-label {
  font-family: var(--cx-font-mono);
  font-size: 10px;
  letter-spacing: 0.12em;
  opacity: 0.85;
}

.article-layout {
  display: grid;
  grid-template-columns: 250px minmax(0, 1fr);
  gap: clamp(32px, 5vw, 72px);
  padding-top: clamp(32px, 5vw, 56px);
}

.rail {
  position: sticky;
  top: 104px;
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: 34px;
}

.rail-block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rail-label {
  font-size: 10px;
}

.search {
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid var(--cx-line-strong);
  padding-bottom: 6px;
}

.search-input {
  flex: 1;
  min-width: 0;
  border: 0;
  background: transparent;
  color: var(--cx-ink);
  font-family: var(--cx-font-mono);
  font-size: 12px;
  letter-spacing: 0.04em;
  outline: none;
  padding: 6px 0;
}

.search-input::placeholder {
  color: var(--cx-ink-mute);
}

.search-submit {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: 0;
  background: transparent;
  color: var(--cx-ink-soft);
  cursor: pointer;
}

.search-submit:hover {
  color: var(--cx-accent);
}

.clear-search {
  align-self: flex-start;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--cx-ink-mute);
  font-size: 10px;
  letter-spacing: 0.06em;
  cursor: pointer;
}

.clear-search:hover {
  color: var(--cx-accent);
}

.tag-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}

.tag-filter .cx-chip {
  cursor: pointer;
  background: transparent;
  transition:
    color 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease;
}

.tag-filter .cx-chip:hover {
  border-color: var(--cx-accent);
  color: var(--cx-accent);
}

.tag-filter .cx-chip.cx-chip--accent,
.tag-filter .cx-chip.cx-chip--accent:hover {
  background: var(--cx-accent);
  border-color: var(--cx-accent);
  color: var(--cx-accent-ink);
}

.rail-meta {
  padding-top: 22px;
  border-top: 1px solid var(--cx-line);
}

.rail-link {
  font-size: 13px;
  color: var(--cx-ink-soft);
}

.rail-link:hover {
  color: var(--cx-accent);
}

.list-area {
  min-width: 0;
}

.list-panel {
  border-radius: var(--cx-radius);
  overflow: hidden;
}

.post-row {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr) 116px;
  gap: 20px;
  padding: clamp(22px, 3vw, 32px);
  border-bottom: 1px solid var(--cx-line);
  transition:
    background 0.3s ease,
    padding 0.3s ease;
}

.post-row:last-child {
  border-bottom: 0;
}

.post-row:hover {
  background: color-mix(in srgb, var(--cx-accent) 5%, transparent);
  padding-left: calc(clamp(22px, 3vw, 32px) + 6px);
}

.post-row.is-featured {
  background: color-mix(in srgb, var(--cx-accent) 6%, transparent);
}

.row-index {
  padding-top: 4px;
  font-size: 11px;
  color: var(--cx-accent);
}

.row-main {
  min-width: 0;
}

.row-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.row-tag {
  font-family: var(--cx-font-mono);
  font-size: 10px;
  letter-spacing: 0.08em;
  color: var(--cx-green);
}

.row-tag::before {
  content: "#";
  margin-right: 2px;
  opacity: 0.6;
}

.row-title {
  margin: 0;
  font-family: var(--cx-font-display);
  font-size: clamp(20px, 2.4vw, 30px);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.28;
  color: var(--cx-ink);
}

.post-row.is-featured .row-title {
  font-size: clamp(26px, 3.6vw, 44px);
  font-weight: 800;
  line-height: 1.15;
}

.row-excerpt {
  margin: 12px 0 0;
  max-width: 62ch;
  font-size: 14px;
  line-height: 1.75;
  color: var(--cx-ink-soft);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.row-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  padding-top: 4px;
  font-family: var(--cx-font-mono);
  font-size: 10px;
  letter-spacing: 0.06em;
  color: var(--cx-ink-mute);
  text-align: right;
}

.row-views {
  color: var(--cx-ink-mute);
}

.empty-state {
  padding: 64px 32px;
  text-align: center;
  border-radius: var(--cx-radius);
}

.empty-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
}

.empty-desc {
  margin: 10px 0 24px;
  color: var(--cx-ink-mute);
  font-size: 14px;
}

.empty-btn {
  padding: 10px 18px;
  border-radius: 999px;
  border: 1px solid var(--cx-line-strong);
  background: transparent;
  cursor: pointer;
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.1em;
}

.empty-btn:hover {
  background: var(--cx-accent);
  border-color: var(--cx-accent);
  color: var(--cx-accent-ink);
}

.loading-state {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.loading-row {
  height: 96px;
  background: var(--cx-line);
  animation: loading-pulse 1.4s ease-in-out infinite;
}

@keyframes loading-pulse {
  0%,
  100% {
    opacity: 0.45;
  }
  50% {
    opacity: 0.9;
  }
}

.pager {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 18px;
  padding-top: 28px;
}

.pager-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 1px solid var(--cx-line-strong);
  background: transparent;
  color: var(--cx-ink);
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.pager-btn:hover:not(:disabled) {
  background: var(--cx-ink);
  color: var(--cx-paper);
}

.pager-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pager-status {
  font-size: 11px;
  letter-spacing: 0.12em;
  color: var(--cx-ink-mute);
}

@media (max-width: 900px) {
  .article-layout {
    grid-template-columns: 1fr;
  }

  .rail {
    position: static;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    padding-bottom: 8px;
  }

  .rail-meta {
    display: none;
  }

  .post-row {
    grid-template-columns: 32px minmax(0, 1fr);
    gap: 14px;
  }

  .row-meta {
    grid-column: 2;
    flex-direction: row;
    align-items: center;
    gap: 14px;
    padding-top: 10px;
    text-align: left;
  }
}

@media (max-width: 640px) {
  .page-hero {
    flex-direction: column;
    align-items: flex-start;
    gap: 24px;
  }

  .hero-count {
    flex-direction: row;
    align-items: baseline;
    gap: 10px;
  }

  .rail {
    grid-template-columns: 1fr;
  }

  .post-row {
    padding: 22px 18px;
    gap: 12px;
  }

  .row-excerpt {
    -webkit-line-clamp: 3;
  }
}
</style>
