<template>
  <div class="comment-item" :style="{ marginLeft: level > 0 ? '24px' : '0' }">
    <div class="comment-header">
      <img
        v-if="comment.user?.avatar_url"
        :src="comment.user.avatar_url"
        class="comment-avatar"
      />
      <div v-else class="comment-avatar placeholder">
        <i class="fa fa-user"></i>
      </div>
      <div class="comment-meta">
        <span class="comment-username">{{ comment.user?.username || '匿名用户' }}</span>
        <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
      </div>
    </div>
    <div class="comment-content">{{ comment.content }}</div>
    <div class="comment-actions">
      <button @click="handleReply" class="action-btn">
        <i class="fa fa-reply"></i> 回复
      </button>
      <button
        v-if="canDelete"
        @click="handleDelete"
        class="action-btn delete"
      >
        <i class="fa fa-trash"></i> 删除
      </button>
    </div>

    <!-- 回复表单 -->
    <div v-if="showReplyForm" class="reply-form">
      <textarea
        v-model="replyContent"
        placeholder="写下你的回复..."
        class="reply-textarea"
      ></textarea>
      <div class="reply-actions">
        <button @click="cancelReply" class="cancel-btn">取消</button>
        <button @click="submitReply" class="submit-btn">发送</button>
      </div>
    </div>

    <!-- 嵌套回复 -->
    <div v-if="comment.replies && comment.replies.length > 0" class="comment-replies">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :level="level + 1"
        :currentUserId="currentUserId"
        @reply="handleNestedReply"
        @delete="handleNestedDelete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import type { Comment } from "../types/comment";

const props = defineProps<{
  comment: Comment;
  level?: number;
  currentUserId?: string;
}>();

const emit = defineEmits<{
  (e: "reply", data: { commentId: number; content: string }): void;
  (e: "delete", commentId: number): void;
}>();

const level = computed(() => props.level || 0);
const showReplyForm = ref(false);
const replyContent = ref("");

const canDelete = computed(() => {
  return props.currentUserId && props.comment.user?.uuid === props.currentUserId;
});

const formatTime = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const handleReply = () => {
  showReplyForm.value = !showReplyForm.value;
};

const cancelReply = () => {
  showReplyForm.value = false;
  replyContent.value = "";
};

const submitReply = () => {
  if (replyContent.value.trim()) {
    emit("reply", {
      commentId: props.comment.id,
      content: replyContent.value.trim(),
    });
    replyContent.value = "";
    showReplyForm.value = false;
  }
};

const handleDelete = () => {
  emit("delete", props.comment.id);
};

const handleNestedReply = (data: { commentId: number; content: string }) => {
  emit("reply", data);
};

const handleNestedDelete = (commentId: number) => {
  emit("delete", commentId);
};
</script>

<style scoped>
.comment-item {
  padding: 16px 0;
  border-bottom: 1px solid var(--color-border, #e1e5e9);
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-avatar.placeholder {
  background: var(--color-bg-secondary, #f5f5f5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-light, #999);
}

.comment-meta {
  display: flex;
  flex-direction: column;
}

.comment-username {
  font-weight: 600;
  color: var(--color-text, #333);
  font-size: 14px;
}

.comment-time {
  font-size: 12px;
  color: var(--color-text-light, #999);
}

.comment-content {
  margin-left: 48px;
  line-height: 1.6;
  color: var(--color-text, #333);
  margin-bottom: 8px;
}

.comment-actions {
  margin-left: 48px;
  display: flex;
  gap: 16px;
}

.action-btn {
  background: none;
  border: none;
  color: var(--color-text-light, #666);
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}

.action-btn:hover {
  color: var(--color-primary, #667eea);
}

.action-btn.delete:hover {
  color: #dc3545;
}

.reply-form {
  margin-left: 48px;
  margin-top: 12px;
}

.reply-textarea {
  width: 100%;
  min-height: 80px;
  padding: 12px;
  border: 1px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 14px;
  margin-bottom: 8px;
}

.reply-textarea:focus {
  outline: none;
  border-color: var(--color-primary, #667eea);
}

.reply-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.cancel-btn,
.submit-btn {
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: var(--color-bg-secondary, #f5f5f5);
  border: 1px solid var(--color-border, #e1e5e9);
  color: var(--color-text, #333);
}

.submit-btn {
  background: var(--color-primary, #667eea);
  border: none;
  color: white;
}

.submit-btn:hover {
  background: var(--color-primary-hover, #5a67d8);
}

.comment-replies {
  margin-top: 8px;
}
</style>
