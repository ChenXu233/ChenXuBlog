<template>
  <article class="comment-item">
    <header class="comment-head">
      <span class="comment-avatar" aria-hidden="true">
        {{ String(comment.user_id).slice(-2) }}
      </span>
      <div class="comment-id">
        <span class="comment-name">用户 #{{ comment.user_id }}</span>
        <time class="comment-time cx-mono" :datetime="String(comment.created_at)">
          {{ formatTime(comment.created_at) }}
        </time>
      </div>
      <div class="comment-actions">
        <button
          v-if="auth.isAuthenticated"
          type="button"
          class="comment-action"
          @click="$emit('reply', comment)"
        >
          回复
        </button>
        <button
          v-if="auth.user?.id === comment.user_id || auth.isAdmin"
          type="button"
          class="comment-action comment-action--danger"
          @click="$emit('delete', comment.id)"
        >
          删除
        </button>
      </div>
    </header>

    <p class="comment-content">{{ comment.content }}</p>

    <div v-if="replies.length" class="replies">
      <div v-for="reply in replies" :key="reply.id" class="reply">
        <header class="reply-head">
          <span class="reply-name">用户 #{{ reply.user_id }}</span>
          <time class="reply-time cx-mono" :datetime="String(reply.created_at)">
            {{ formatTime(reply.created_at) }}
          </time>
          <button
            v-if="auth.user?.id === reply.user_id || auth.isAdmin"
            type="button"
            class="comment-action comment-action--danger reply-delete"
            @click="$emit('delete', reply.id)"
          >
            删除
          </button>
        </header>
        <p class="reply-content">{{ reply.content }}</p>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { Comment } from "~/api-client/types.gen";

defineProps<{
  comment: Comment;
  replies: Comment[];
  authUserId?: number;
}>();

defineEmits<{ reply: [Comment]; delete: [number] }>();

const auth = useAuthStore();

function formatTime(ts: string | number | Date): string {
  const d = new Date(ts);
  return d.toLocaleString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}
</script>

<style scoped>
.comment-item {
  padding: 22px 0;
  border-bottom: 1px solid var(--cx-line);
}

.comment-head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-avatar {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex-shrink: 0;
  background: var(--cx-accent);
  color: var(--cx-accent-ink);
  font-family: var(--cx-font-mono);
  font-size: 10px;
  font-weight: 700;
}

.comment-id {
  min-width: 0;
  display: flex;
  align-items: baseline;
  gap: 10px;
  flex-wrap: wrap;
}

.comment-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--cx-ink);
}

.comment-time {
  font-size: 10px;
  letter-spacing: 0.06em;
  color: var(--cx-ink-mute);
}

.comment-actions {
  margin-left: auto;
  display: flex;
  gap: 12px;
}

.comment-action {
  padding: 0;
  border: 0;
  background: transparent;
  font-family: var(--cx-font-mono);
  font-size: 10px;
  letter-spacing: 0.08em;
  color: var(--cx-ink-mute);
  cursor: pointer;
}

.comment-action:hover {
  color: var(--cx-accent);
}

.comment-action--danger:hover {
  color: #d33;
}

.comment-content {
  margin: 12px 0 0 46px;
  font-size: 14px;
  line-height: 1.8;
  color: var(--cx-ink-soft);
  white-space: pre-wrap;
  overflow-wrap: break-word;
}

.replies {
  margin: 16px 0 0 46px;
  padding-left: 18px;
  border-left: 1px solid var(--cx-line-strong);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reply-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.reply-name {
  font-size: 12px;
  font-weight: 700;
  color: var(--cx-ink);
}

.reply-time {
  font-size: 10px;
  color: var(--cx-ink-mute);
}

.reply-delete {
  margin-left: auto;
}

.reply-content {
  margin: 6px 0 0;
  font-size: 13px;
  line-height: 1.8;
  color: var(--cx-ink-soft);
  white-space: pre-wrap;
}

@media (max-width: 640px) {
  .comment-content,
  .replies {
    margin-left: 0;
  }
}
</style>
