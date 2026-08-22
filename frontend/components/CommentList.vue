<template>
  <div class="space-y-4">
    <!-- Comment form -->
    <div
      v-if="auth.isAuthenticated"
      class="bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700"
    >
      <UTextarea
        v-model="newComment"
        :rows="3"
        placeholder="写下你的评论…"
        class="mb-2"
      />
      <div class="flex justify-end">
        <UButton
          color="primary"
          size="sm"
          :loading="submitting"
          @click="submitComment(null)"
        >
          发表评论
        </UButton>
      </div>
    </div>
    <div
      v-else
      class="text-sm text-gray-500 bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700"
    >
      <NuxtLink to="/login" class="text-primary-500">登录</NuxtLink> 后参与评论
    </div>

    <!-- Comment list -->
    <div v-if="comments.length" class="space-y-3">
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
    <p v-else class="text-gray-400 text-sm text-center py-8">
      暂无评论，快来抢沙发！
    </p>

    <!-- Reply box -->
    <UModal v-model="replyModalOpen">
      <div class="p-4">
        <h3 class="font-semibold mb-3">
          回复 {{ replyTarget?.content?.slice(0, 20) }}…
        </h3>
        <UTextarea
          v-model="replyContent"
          :rows="3"
          placeholder="写下你的回复…"
          class="mb-2"
        />
        <div class="flex justify-end gap-2">
          <UButton
            variant="ghost"
            size="sm"
            @click="
              () => {
                replyModalOpen = false;
              }
            "
            >取消</UButton
          >
          <UButton
            color="primary"
            size="sm"
            :loading="submitting"
            @click="submitReply"
            >回复</UButton
          >
        </div>
      </div>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import { commentService } from "../service/comment";
import type { Comment } from "../src/client/types.gen";

const props = defineProps<{
  blogId: number;
}>();

const auth = useAuthStore();
const comments = ref<Comment[]>([]);

async function load() {
  const res = await commentService.getComments(props.blogId);
  comments.value = res.comments || [];
}

watch(() => props.blogId, load, { immediate: true });

const newComment = ref("");
const replyContent = ref("");
const replyModalOpen = ref(false);
const replyTarget = ref<Comment | null>(null);
const submitting = ref(false);

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
</script>
