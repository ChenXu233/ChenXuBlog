<template>
  <div
    class="bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700"
  >
    <div class="flex justify-between items-start mb-2">
      <div class="flex items-center gap-2">
        <UAvatar :alt="'用户' + comment.user_id" size="sm" class="shrink-0" />
        <span class="font-medium text-sm">用户 #{{ comment.user_id }}</span>
        <span class="text-xs text-gray-400">{{
          formatTime(comment.created_at)
        }}</span>
      </div>
      <div class="flex gap-1">
        <UButton
          v-if="auth.isAuthenticated"
          icon="i-heroicons-chat-bubble-left-ellipsis"
          size="xs"
          variant="ghost"
          @click="$emit('reply', comment)"
        />
        <UButton
          v-if="auth.user?.id === comment.user_id || auth.isAdmin"
          icon="i-heroicons-trash"
          size="xs"
          variant="ghost"
          color="error"
          @click="$emit('delete', comment.id)"
        />
      </div>
    </div>
    <p class="text-sm whitespace-pre-wrap">{{ comment.content }}</p>

    <!-- Nested replies -->
    <div
      v-if="replies.length"
      class="mt-3 space-y-2 border-l-2 border-slate-200 dark:border-slate-700 pl-3"
    >
      <div
        v-for="reply in replies"
        :key="reply.id"
        class="bg-slate-50 dark:bg-slate-700/30 rounded-lg p-3"
      >
        <div class="flex justify-between items-start mb-1">
          <div class="flex items-center gap-2">
            <UAvatar :alt="'用户' + reply.user_id" size="xs" class="shrink-0" />
            <span class="font-medium text-xs">用户 #{{ reply.user_id }}</span>
            <span class="text-xs text-gray-400">{{
              formatTime(reply.created_at)
            }}</span>
          </div>
          <UButton
            v-if="auth.user?.id === reply.user_id || auth.isAdmin"
            icon="i-heroicons-trash"
            size="xs"
            variant="ghost"
            color="error"
            @click="$emit('delete', reply.id)"
          />
        </div>
        <p class="text-sm">{{ reply.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Comment } from "~/shared/api-client/types.gen";

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
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
</script>
