<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <div class="max-w-6xl mx-auto px-4 py-8">
      <div v-if="article" class="flex gap-8">
        <!-- Main content -->
        <article class="flex-1 min-w-0">
          <template v-if="article.cover_url">
            <img
              :src="article.cover_url"
              :alt="article.title"
              class="w-full h-64 object-cover rounded-xl mb-6"
            />
          </template>
          <h1 class="text-4xl font-bold mb-4">{{ article.title }}</h1>
          <div class="flex items-center gap-4 text-gray-500 text-sm mb-6">
            <span>{{ formatDate(article.created_at) }}</span>
            <span>{{ article.view_count }} 次阅读</span>
            <span>{{ article.likes_count }} 赞</span>
            <div class="flex gap-1">
              <UBadge
                v-for="tag in article.tags_name"
                :key="tag"
                variant="soft"
                size="sm"
                >{{ tag }}</UBadge
              >
            </div>
          </div>
          <div
            class="prose dark:prose-invert max-w-none markdown-body"
            v-html="rendered.html"
          ></div>

          <!-- Comments -->
          <div class="mt-12">
            <h2 class="text-2xl font-bold mb-4">
              评论（{{ comments.length }}）
            </h2>
            <CommentList
              :blog-id="article.id"
              :comments="comments"
              @deleted="loadComments"
            />
          </div>
        </article>

        <!-- TOC sidebar -->
        <aside v-if="rendered.toc.length" class="hidden lg:block w-56 shrink-0">
          <div
            class="sticky top-8 bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700"
          >
            <div class="text-sm font-semibold mb-3 text-gray-500">目录</div>
            <nav class="space-y-1 text-sm">
              <a
                v-for="item in rendered.toc"
                :key="item.id"
                :href="`#${item.id}`"
                class="block hover:text-primary-500 transition-colors"
                :style="{ paddingLeft: `${(item.level - 2) * 12}px` }"
              >
                {{ item.title }}
              </a>
            </nav>
          </div>
        </aside>
      </div>

      <div v-else class="text-center py-20">
        <p class="text-gray-500 mb-4">文章不存在或已删除</p>
        <UButton to="/article" variant="ghost">返回文章列表</UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Article } from "~/types/article";
import { renderMarkdown } from "~/utils/markdown";

const route = useRoute();
const { data } = await useApiFetch<Article>(`/blog/${route.params.id}`);
const article = computed(() => data.value || null);

useSeo({
  title: article.value?.title,
  description: article.value?.body?.slice(0, 150),
  image: article.value?.cover_url,
  type: "article",
});

const rendered = computed(() => {
  const body = article.value?.body || "";
  return renderMarkdown(body);
});

function formatDate(ts: string | number): string {
  const d = typeof ts === "number" ? new Date(ts * 1000) : new Date(ts);
  return d.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// Comments
interface CommentItem {
  id: number;
  content: string;
  created_at: string;
  user_id: number;
  reply_to_id: number | null;
}

const comments = ref<CommentItem[]>([]);
async function loadComments() {
  if (!article.value) return;
  const resp = await $fetch<{ comments: CommentItem[] }>(
    import.meta.server
      ? `${
          process.env.NUXT_API_INTERNAL_URL || "http://127.0.0.1:8001"
        }/apis/v1/comment/get/${article.value.id}`
      : `/apis/v1/comment/get/${article.value.id}`,
  );
  comments.value = resp.comments || [];
}
// 评论在客户端加载（SSR 端 $fetch 相对路径会 404）
if (import.meta.client) {
  await loadComments();
}
</script>

<style scoped>
@reference "~/assets/css/main.css";

.markdown-body :deep(pre) {
  @apply rounded-lg p-4 overflow-x-auto bg-slate-100 dark:bg-slate-800 mb-4;
}
.markdown-body :deep(code) {
  @apply font-mono text-sm;
}
.markdown-body :deep(code:not(pre code)) {
  @apply bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded text-rose-500;
}
.markdown-body :deep(h2) {
  @apply text-2xl font-bold mt-8 mb-4;
}
.markdown-body :deep(h3) {
  @apply text-xl font-bold mt-6 mb-3;
}
.markdown-body :deep(p) {
  @apply my-4 leading-relaxed;
}
.markdown-body :deep(ul) {
  @apply list-disc pl-6 my-4;
}
.markdown-body :deep(ol) {
  @apply list-decimal pl-6 my-4;
}
.markdown-body :deep(a) {
  @apply text-primary-500 underline;
}
.markdown-body :deep(blockquote) {
  @apply border-l-4 border-slate-300 dark:border-slate-600 pl-4 my-4 text-gray-500 italic;
}
.markdown-body :deep(img) {
  @apply rounded-lg my-4 max-w-full;
}
</style>
