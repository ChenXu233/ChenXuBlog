<template>
  <div class="markdown-editor">
    <div class="editor-toolbar">
      <button
        v-for="tool in tools"
        :key="tool.name"
        @click="tool.action"
        :title="tool.title"
        class="tool-btn"
        :disabled="uploading && tool.name === 'image'"
      >
        <i :class="tool.icon"></i>
      </button>
      <span v-if="uploading" class="upload-indicator">
        <i class="fa fa-spinner fa-spin"></i> 上传中...
      </span>
    </div>
    <div class="editor-container">
      <div class="editor-pane">
        <textarea
          ref="textareaRef"
          v-model="content"
          @input="handleInput"
          @keydown.tab.prevent="handleTab"
          placeholder="使用 Markdown 编写..."
        ></textarea>
      </div>
      <div class="preview-pane" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import MarkdownIt from "markdown-it";
import { imgBedService } from "../service/imgBed";

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

const textareaRef = ref<HTMLTextAreaElement | null>(null);
const content = ref(props.modelValue);
const uploading = ref(false);

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal !== content.value) {
      content.value = newVal;
    }
  }
);

const renderedContent = computed(() => {
  return md.render(content.value);
});

const handleInput = () => {
  emit("update:modelValue", content.value);
};

const insertText = (before: string, after: string = "") => {
  const textarea = textareaRef.value;
  if (!textarea) return;

  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const selected = content.value.substring(start, end);

  content.value =
    content.value.substring(0, start) +
    before +
    selected +
    after +
    content.value.substring(end);

  emit("update:modelValue", content.value);

  setTimeout(() => {
    textarea.focus();
    textarea.setSelectionRange(
      start + before.length,
      start + before.length + selected.length
    );
  }, 0);
};

const handleImageUpload = () => {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;

    uploading.value = true;
    try {
      const { url } = await imgBedService.uploadImg(file);
      insertText(`![${file.name}](${url})`, "");
    } catch (error) {
      console.error("图片上传失败:", error);
    } finally {
      uploading.value = false;
    }
  };
  input.click();
};

const tools = [
  { name: "bold", title: "粗体", icon: "fa fa-bold", action: () => insertText("**", "**") },
  { name: "italic", title: "斜体", icon: "fa fa-italic", action: () => insertText("*", "*") },
  { name: "heading", title: "标题", icon: "fa fa-header", action: () => insertText("## ") },
  { name: "link", title: "链接", icon: "fa fa-link", action: () => insertText("[", "](url)") },
  { name: "image", title: "图片", icon: "fa fa-image", action: handleImageUpload },
  { name: "code", title: "代码", icon: "fa fa-code", action: () => insertText("`", "`") },
  { name: "codeBlock", title: "代码块", icon: "fa fa-file-code-o", action: () => insertText("\n```\n", "\n```\n") },
  { name: "quote", title: "引用", icon: "fa fa-quote-left", action: () => insertText("> ") },
  { name: "list", title: "列表", icon: "fa fa-list-ul", action: () => insertText("- ") },
  { name: "orderedList", title: "有序列表", icon: "fa fa-list-ol", action: () => insertText("1. ") },
  { name: "hr", title: "分割线", icon: "fa fa-minus", action: () => insertText("\n---\n") },
];

const handleTab = (e: KeyboardEvent) => {
  insertText("  ");
};
</script>

<style scoped>
.markdown-editor {
  border: 1px solid var(--color-border, #e1e5e9);
  border-radius: 8px;
  overflow: hidden;
  background: var(--color-bg, white);
}

.editor-toolbar {
  display: flex;
  gap: 4px;
  padding: 8px;
  background: var(--color-bg-secondary, #f5f5f5);
  border-bottom: 1px solid var(--color-border, #e1e5e9);
  flex-wrap: wrap;
}

.tool-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  color: var(--color-text-light, #666);
  transition: all 0.2s;
}

.tool-btn:hover:not(:disabled) {
  background: var(--color-primary, #667eea);
  color: white;
}

.tool-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.upload-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  font-size: 12px;
  color: #667eea;
  margin-left: auto;
}

.editor-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 400px;
}

.editor-pane {
  border-right: 1px solid var(--color-border, #e1e5e9);
}

.editor-pane textarea {
  width: 100%;
  height: 100%;
  min-height: 400px;
  padding: 16px;
  border: none;
  resize: none;
  font-family: "Consolas", "Monaco", monospace;
  font-size: 14px;
  line-height: 1.6;
  background: var(--color-bg, white);
  color: var(--color-text, #333);
}

.editor-pane textarea:focus {
  outline: none;
}

.preview-pane {
  padding: 16px;
  overflow-y: auto;
  min-height: 400px;
  background: var(--color-bg, white);
}

.preview-pane :deep(h1),
.preview-pane :deep(h2),
.preview-pane :deep(h3) {
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.preview-pane :deep(p) {
  margin-bottom: 1em;
  line-height: 1.8;
}

.preview-pane :deep(code) {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "Consolas", monospace;
}

.preview-pane :deep(pre) {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}

.preview-pane :deep(pre code) {
  background: none;
  padding: 0;
}

.preview-pane :deep(blockquote) {
  border-left: 4px solid var(--color-primary, #667eea);
  padding-left: 16px;
  margin: 16px 0;
  color: var(--color-text-light, #666);
}

@media (max-width: 768px) {
  .editor-container {
    grid-template-columns: 1fr;
  }

  .editor-pane {
    border-right: none;
    border-bottom: 1px solid var(--color-border, #e1e5e9);
  }
}
</style>
