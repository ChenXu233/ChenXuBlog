<template>
  <div class="comment-list">
    <h3 class="comment-title">
      <i class="fa fa-comments"></i> 评论 ({{ totalCount }})
    </h3>

    <!-- 评论输入框 -->
    <div v-if="isAuthenticated" class="comment-form">
      <textarea
        v-model="newComment"
        placeholder="写下你的评论..."
        class="comment-textarea"
      ></textarea>
      <button @click="submitComment" class="submit-btn" :disabled="!newComment.trim()">
       发表评论
      </button>
    </div>
    <div v-else class="login-hint">
      <router-link to="/login">登录</router-link> 后才能评论
    </div>

    <!-- 评论列表 -->
    <div v-if="loading" class="loading">
      <i class="fa fa-spinner fa-spin"></i> 加载中...
    </div>
    <div v-else-if="comments.length === 0" class="empty">
      暂无评论，来抢沙发吧！
    </div>
    <div v-else class="comments">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :currentUserId="currentUserId"
        @reply="handleReply"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import CommentItem from "./CommentItem.vue";
import { commentService } from "../service/comment";
import { useTokenStore } from "../stores/token";
import { useUserStore } from "../stores/userStore";
import { showError } from "../utils/request";
import type { Comment } from "../types/comment";

const props = defineProps<{
  blogId: number;
}>();

const tokenStore = useTokenStore();
const userStore = useUserStore();

const comments = ref<Comment[]>([]);
const loading = ref(false);
const newComment = ref("");

const isAuthenticated = computed(() => tokenStore.isAuthenticated);
const currentUserId = computed(() => userStore.id);

const totalCount = computed(() => {
  let count = 0;
  const countReplies = (list: Comment[]) => {
    for (const c of list) {
      count++;
      if (c.replies && c.replies.length > 0) {
        countReplies(c.replies);
      }
    }
  };
  countReplies(comments.value);
  return count;
});

const buildCommentTree = (flatComments: Comment[]): Comment[] => {
  const map = new Map<number, Comment>();
  const roots: Comment[] = [];

  flatComments.forEach((c) => {
    map.set(c.id, { ...c, replies: [] });
  });

  flatComments.forEach((c) => {
    const node = map.get(c.id)!;
    if (c.reply_to_id && map.has(c.reply_to_id)) {
      map.get(c.reply_to_id)!.replies!.push(node);
    } else {
      roots.push(node);
    }
  });

  return roots;
};

const fetchComments = async () => {
  loading.value = true;
  try {
    const res = await commentService.getComments(props.blogId);
    comments.value = buildCommentTree(res.comments);
  } catch (error) {
    showError("加载评论失败");
  } finally {
    loading.value = false;
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) return;

  try {
    await commentService.createComment({
      blog_id: props.blogId,
      content: newComment.value.trim(),
    });
    newComment.value = "";
    await fetchComments();
  } catch (error) {
    showError("发表评论失败");
  }
};

const handleReply = async (data: { commentId: number; content: string }) => {
  try {
    await commentService.createComment({
      blog_id: props.blogId,
      content: data.content,
      reply_to_id: data.commentId,
    });
    await fetchComments();
  } catch (error) {
    showError("回复失败");
  }
};

const handleDelete = async (commentId: number) => {
  try {
    await commentService.deleteComment(commentId);
    await fetchComments();
  } catch (error) {
    showError("删除评论失败");
  }
};

onMounted(() => {
  fetchComments();
});

defineExpose({ fetchComments });
</script>

<style scoped>
.comment-list {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border, #e1e5e9);
}

.comment-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text, #333);
}

.comment-form {
  margin-bottom: 24px;
}

.comment-textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 14px;
  margin-bottom: 12px;
}

.comment-textarea:focus {
  outline: none;
  border-color: var(--color-primary, #667eea);
}

.submit-btn {
  background: var(--color-primary, #667eea);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: var(--color-primary-hover, #5a67d8);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-hint {
  margin-bottom: 24px;
  padding: 16px;
  background: var(--color-bg-secondary, #f5f5f5);
  border-radius: 8px;
  text-align: center;
  color: var(--color-text-light, #666);
}

.login-hint a {
  color: var(--color-primary, #667eea);
  text-decoration: none;
  font-weight: 500;
}

.login-hint a:hover {
  text-decoration: underline;
}

.loading,
.empty {
  text-align: center;
  padding: 32px;
  color: var(--color-text-light, #999);
}

.comments {
  margin-top: 16px;
}
</style>
