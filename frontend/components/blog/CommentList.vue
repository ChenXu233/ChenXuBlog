<template>
  <div class="comment-list">
    <div v-if="auth.isAuthenticated" class="comment-form cx-glass">
      <label class="form-label cx-eyebrow" for="new-comment">写点什么</label>
      <textarea
        id="new-comment"
        v-model="newComment"
        class="comment-textarea"
        rows="3"
        placeholder="写下你的评论…"
      />
      <div class="form-actions">
        <span class="form-hint cx-mono">CTRL + ENTER 发送</span>
        <button
          type="button"
          class="submit-btn"
          :disabled="submitting || !newComment.trim()"
          @click="submitComment(null)"
        >
          {{ submitting ? "发送中…" : "发表评论" }}
        </button>
      </div>
    </div>

    <div v-else class="login-hint">
      <NuxtLink to="/login" class="login-link">登录</NuxtLink>
      <span>后参与评论</span>
    </div>

    <div v-if="comments.length" class="comments">
      <CommentItem
        v-for="comment in topLevelComments"
        :key="comment.id"
        :comment="comment"
        :replies="repliesOf(comment.id)"
        :auth-user-id="auth.user?.id"
        @reply="startReply"
        @delete="deleteComment"
      />
    </div>
    <p v-else class="empty">暂无评论，快来抢沙发！</p>

    <div
      v-if="replyModalOpen"
      class="reply-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="回复评论"
      @click.self="replyModalOpen = false"
    >
      <div class="reply-dialog">
        <header class="reply-dialog-head">
          <h3>回复</h3>
          <button type="button" class="close-btn" aria-label="关闭" @click="replyModalOpen = false">
            ×
          </button>
        </header>
        <p class="reply-target">{{ replyTarget?.content?.slice(0, 60) }}…</p>
        <textarea
          v-model="replyContent"
          class="comment-textarea"
          rows="3"
          placeholder="写下你的回复…"
        />
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="replyModalOpen = false">
            取消
          </button>
          <button
            type="button"
            class="submit-btn"
            :disabled="submitting || !replyContent.trim()"
            @click="submitReply"
          >
            {{ submitting ? "发送中…" : "回复" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Comment } from "~/api-client/types.gen";
import { commentService } from "~/service/comment";

const props = defineProps<{
  blogId: number;
}>();

const auth = useAuthStore();
const comments = ref<Comment[]>([]);
const newComment = ref("");
const replyContent = ref("");
const replyModalOpen = ref(false);
const replyTarget = ref<Comment | null>(null);
const submitting = ref(false);

async function load() {
  try {
    const res = await commentService.getComments(props.blogId);
    comments.value = res.comments || [];
  } catch {
    comments.value = [];
  }
}

watch(() => props.blogId, load, { immediate: true });

const topLevelComments = computed(() =>
  comments.value.filter((c) => !c.reply_to_id),
);

function repliesOf(id: number): Comment[] {
  return comments.value.filter((c) => c.reply_to_id === id);
}

async function submitComment(replyToId: number | null) {
  const content = replyToId === null ? newComment.value : replyContent.value;
  if (!content.trim()) return;
  submitting.value = true;
  try {
    await commentService.createComment({
      blog_id: props.blogId,
      content: content.trim(),
      ...(replyToId ? { reply_to_id: replyToId } : {}),
    });
    newComment.value = "";
    replyModalOpen.value = false;
    useToast().add({ title: "评论成功", color: "success" });
    await load();
  } catch (e: any) {
    useToast().add({ title: e?.message || "评论失败", color: "error" });
  } finally {
    submitting.value = false;
  }
}

function startReply(comment: Comment) {
  replyTarget.value = comment;
  replyContent.value = "";
  replyModalOpen.value = true;
}

async function submitReply() {
  if (!replyTarget.value) return;
  await submitComment(replyTarget.value.id);
}

async function deleteComment(id: number) {
  if (!confirm("确定删除该评论？")) return;
  try {
    await commentService.deleteComment(id);
    useToast().add({ title: "评论已删除", color: "success" });
    await load();
  } catch (e: any) {
    useToast().add({ title: e?.message || "删除失败", color: "error" });
  }
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === "Escape") replyModalOpen.value = false;
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    if (replyModalOpen.value) submitReply();
    else if (auth.isAuthenticated) submitComment(null);
  }
}

onMounted(() => window.addEventListener("keydown", onKeydown));
onBeforeUnmount(() => window.removeEventListener("keydown", onKeydown));
</script>

<style scoped>
.comment-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.comment-form {
  padding: 22px;
  border-radius: var(--cx-radius);
}

.form-label {
  display: block;
  margin-bottom: 12px;
  font-size: 10px;
}

.comment-textarea {
  width: 100%;
  resize: vertical;
  min-height: 92px;
  padding: 14px;
  border-radius: 14px;
  border: 1px solid var(--cx-line);
  background: color-mix(in srgb, var(--cx-paper) 60%, transparent);
  color: var(--cx-ink);
  font-family: var(--cx-font-sans);
  font-size: 14px;
  line-height: 1.7;
  outline: none;
  transition: border-color 0.2s ease;
}

.comment-textarea:focus {
  border-color: var(--cx-accent);
}

.form-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 14px;
}

.form-hint {
  margin-right: auto;
  font-size: 9px;
  letter-spacing: 0.1em;
  color: var(--cx-ink-mute);
}

.submit-btn {
  padding: 10px 20px;
  border-radius: 999px;
  border: 1px solid var(--cx-accent);
  background: var(--cx-accent);
  color: var(--cx-accent-ink);
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.submit-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.cancel-btn {
  padding: 10px 18px;
  border-radius: 999px;
  border: 1px solid var(--cx-line-strong);
  background: transparent;
  font-family: var(--cx-font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  cursor: pointer;
}

.login-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 18px 22px;
  border-radius: var(--cx-radius-sm);
  border: 1px dashed var(--cx-line-strong);
  font-size: 13px;
  color: var(--cx-ink-mute);
}

.login-link {
  color: var(--cx-accent);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.comments {
  margin-top: 22px;
}

.empty {
  padding: 40px 0;
  text-align: center;
  font-size: 13px;
  color: var(--cx-ink-mute);
}

.reply-overlay {
  position: fixed;
  inset: 0;
  z-index: 120;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(10, 10, 10, 0.55);
  backdrop-filter: blur(6px);
}

.reply-dialog {
  width: min(520px, 100%);
  padding: 24px;
  border-radius: var(--cx-radius);
  background: var(--cx-surface);
  border: 1px solid var(--cx-line-strong);
  box-shadow: var(--cx-shadow);
}

.reply-dialog-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.reply-dialog-head h3 {
  margin: 0;
  font-family: var(--cx-font-display);
  font-size: 22px;
  font-weight: 800;
}

.close-btn {
  border: 0;
  background: transparent;
  font-size: 22px;
  line-height: 1;
  color: var(--cx-ink-mute);
  cursor: pointer;
}

.reply-target {
  margin: 12px 0;
  padding-left: 12px;
  border-left: 2px solid var(--cx-accent);
  font-size: 12px;
  line-height: 1.7;
  color: var(--cx-ink-mute);
}
</style>
