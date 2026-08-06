<template>
  <div class="article-editor">
    <div class="editor-header">
      <h2>{{ isEdit ? '编辑文章' : '创建文章' }}</h2>
      <div class="header-actions">
        <button @click="goBack" class="cancel-btn">取消</button>
        <button @click="saveDraft" class="draft-btn" :disabled="saving">
          保存草稿
        </button>
        <button @click="publish" class="publish-btn" :disabled="saving">
          {{ saving ? '发布中...' : '发布' }}
        </button>
      </div>
    </div>

    <div class="editor-body">
      <div class="form-group">
        <input
          v-model="form.title"
          type="text"
          placeholder="文章标题"
          class="title-input"
        />
      </div>

      <div class="form-row">
        <div class="form-group flex-1">
          <label>标签（用逗号分隔）</label>
          <input
            v-model="tagsInput"
            type="text"
            placeholder="技术, Vue, 前端"
            class="tags-input"
          />
        </div>
        <div class="form-group">
          <label>封面图片 URL</label>
          <input
            v-model="form.cover_url"
            type="text"
            placeholder="https://..."
            class="cover-input"
          />
        </div>
      </div>

      <div class="form-group">
        <label>正文内容（Markdown）</label>
        <MarkdownEditor v-model="form.body" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import MarkdownEditor from "../components/MarkdownEditor.vue";
import { blogService } from "../service/blog";
import { useTokenStore } from "../stores/token";
import { showError } from "../utils/request";
import type { ArticleCreate } from "../types/article";

const route = useRoute();
const router = useRouter();
const tokenStore = useTokenStore();

const isEdit = computed(() => !!route.params.id);
const articleId = computed(() =>
  isEdit.value ? Number(route.params.id) : null
);

const form = ref<ArticleCreate>({
  title: "",
  body: "",
  tags_name: [],
  cover_url: "",
  published: false,
});

const tagsInput = ref("");
const saving = ref(false);

const parseTags = (input: string): string[] => {
  return input
    .split(",")
    .map((t) => t.trim())
    .filter((t) => t.length > 0);
};

const goBack = () => {
  router.back();
};

const saveDraft = async () => {
  saving.value = true;
  try {
    const data: ArticleCreate = {
      ...form.value,
      tags_name: parseTags(tagsInput.value),
      published: false,
    };

    if (isEdit.value && articleId.value) {
      await blogService.updateBlog(articleId.value, data);
      showError("草稿已保存", "提示", "success");
    } else {
      await blogService.createBlog(data);
      showError("草稿已保存", "提示", "success");
    }
    router.push("/home");
  } catch (error) {
    showError("保存失败");
  } finally {
    saving.value = false;
  }
};

const publish = async () => {
  if (!form.value.title.trim()) {
    showError("请输入文章标题");
    return;
  }
  if (!form.value.body.trim()) {
    showError("请输入文章内容");
    return;
  }

  saving.value = true;
  try {
    const data: ArticleCreate = {
      ...form.value,
      tags_name: parseTags(tagsInput.value),
      published: true,
    };

    if (isEdit.value && articleId.value) {
      await blogService.updateBlog(articleId.value, data);
    } else {
      await blogService.createBlog(data);
    }
    showError("发布成功", "提示", "success");
    router.push("/home");
  } catch (error) {
    showError("发布失败");
  } finally {
    saving.value = false;
  }
};

const fetchArticle = async () => {
  if (!articleId.value) return;
  try {
    const article = await blogService.getBlog(articleId.value);
    form.value = {
      title: article.title,
      body: article.body,
      tags_name: article.tags_name,
      cover_url: article.cover_url || "",
      published: article.published,
    };
    tagsInput.value = article.tags_name?.join(", ") || "";
  } catch (error) {
    showError("加载文章失败");
  }
};

onMounted(() => {
  if (!tokenStore.isAuthenticated) {
    showError("请先登录");
    router.push("/login");
    return;
  }
  if (isEdit.value) {
    fetchArticle();
  }
});
</script>

<style scoped>
.article-editor {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border, #e1e5e9);
}

.editor-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.cancel-btn,
.draft-btn,
.publish-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: var(--color-bg-secondary, #f5f5f5);
  border: 1px solid var(--color-border, #e1e5e9);
  color: var(--color-text, #333);
}

.draft-btn {
  background: white;
  border: 1px solid var(--color-primary, #667eea);
  color: var(--color-primary, #667eea);
}

.publish-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.cancel-btn:hover {
  background: var(--color-border, #e1e5e9);
}

.draft-btn:hover {
  background: var(--color-primary, #667eea);
  color: white;
}

.publish-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.publish-btn:disabled,
.draft-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.editor-body {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text, #333);
}

.form-row {
  display: flex;
  gap: 20px;
}

.flex-1 {
  flex: 1;
}

.title-input {
  width: 100%;
  padding: 16px;
  border: 2px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  font-size: 20px;
  font-weight: 600;
  transition: border-color 0.2s;
}

.title-input:focus {
  outline: none;
  border-color: var(--color-primary, #667eea);
}

.tags-input,
.cover-input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.tags-input:focus,
.cover-input:focus {
  outline: none;
  border-color: var(--color-primary, #667eea);
}

@media (max-width: 768px) {
  .editor-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .form-row {
    flex-direction: column;
  }
}
</style>
