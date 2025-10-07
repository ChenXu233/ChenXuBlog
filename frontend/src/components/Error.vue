<template>
  <div class="error-container" :class="errorType" v-if="show">
    <div class="error-content">
      <div class="error-icon">
        <i v-if="errorType === 'error'" class="fa fa-exclamation-triangle"></i>
        <i v-else-if="errorType === 'warning'" class="fa fa-warning"></i>
        <i v-else-if="errorType === 'info'" class="fa fa-info-circle"></i>
        <i v-else-if="errorType === 'success'" class="fa fa-check-circle"></i>
      </div>
      <div class="error-text">
        <h3 v-if="title">{{ title }}</h3>
        <p>{{ message }}</p>
        <div v-if="details" class="error-details">
          <p class="details-label">详细信息:</p>
          <pre>{{ details }}</pre>
        </div>
      </div>
      <button @click="handleClose" class="error-close-btn">×</button>
    </div>
    <div class="error-actions" v-if="showActions">
      <button @click="handleRetry" class="error-retry-btn" v-if="onRetry">
        重试
      </button>
      <button @click="handleClose" class="error-cancel-btn">关闭</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";

// 定义错误类型
const ErrorType = ["error", "warning", "info", "success"] as const;
export type ErrorType = (typeof ErrorType)[number];

// 定义组件属性
interface ErrorProps {
  message: string;
  title?: string;
  type?: ErrorType;
  details?: string;
  show?: boolean;
  autoHide?: boolean;
  autoHideDuration?: number;
  showActions?: boolean;
  onRetry?: () => void;
}

// 定义组件事件
const emit = defineEmits<{
  close: [];
  retry: [];
}>();

// 定义组件属性和默认值
const props = withDefaults(defineProps<ErrorProps>(), {
  title: "",
  type: "error",
  show: true,
  autoHide: false,
  autoHideDuration: 5000,
  showActions: true,
  details: "",
});

// 内部状态，用于控制组件显示
const show = ref(props.show);
const errorType = ref<ErrorType>(props.type);
let autoHideTimer: ReturnType<typeof setTimeout> | null = null;

// 监听属性变化
watch(
  () => props.show,
  (newVal) => {
    show.value = newVal;
    handleAutoHide();
  },
);

watch(
  () => props.type,
  (newType) => {
    if (ErrorType.includes(newType)) {
      errorType.value = newType;
    }
  },
);

// 自动隐藏处理
const handleAutoHide = () => {
  if (autoHideTimer) {
    clearTimeout(autoHideTimer);
  }

  if (props.autoHide && show.value) {
    autoHideTimer = setTimeout(() => {
      handleClose();
    }, props.autoHideDuration);
  }
};

// 关闭处理
const handleClose = () => {
  show.value = false;
  emit("close");
};

// 重试处理
const handleRetry = () => {
  emit("retry");
  if (props.onRetry) {
    props.onRetry();
  }
};

// 组件挂载时初始化自动隐藏
onMounted(() => {
  handleAutoHide();
});
</script>

<style scoped>
.error-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  max-width: 500px;
  width: 90%;
  border-radius: 12px;
  padding: 20px;
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: fadeIn 0.3s ease-out;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
}

/* 不同类型的错误样式 */
.error-container.error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.error-container.warning {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.error-container.info {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.error-container.success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.error-content {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.error-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.error-text {
  flex: 1;
  min-width: 0;
}

.error-text h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #111827;
}

.error-text p {
  color: #4b5563;
  margin-bottom: 12px;
  line-height: 1.5;
}

.error-details {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  padding: 12px;
  margin-top: 12px;
  font-size: 14px;
}

.details-label {
  font-weight: 600;
  margin-bottom: 8px !important;
}

.error-details pre {
  white-space: pre-wrap;
  word-break: break-word;
  color: #374151;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
  line-height: 1.4;
  margin: 0;
}

.error-close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.error-close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #374151;
}

.error-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 16px;
}

.error-retry-btn,
.error-cancel-btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.error-retry-btn::before,
.error-cancel-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: all 0.4s ease;
  z-index: -1;
}

.error-retry-btn:hover::before,
.error-cancel-btn:hover::before {
  left: 100%;
}

.error-retry-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  box-shadow:
    0 4px 6px -1px rgba(59, 130, 246, 0.2),
    0 2px 4px -1px rgba(59, 130, 246, 0.1);
}

.error-retry-btn:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px);
  box-shadow:
    0 6px 10px -1px rgba(59, 130, 246, 0.3),
    0 4px 6px -1px rgba(59, 130, 246, 0.2);
}

.error-cancel-btn {
  background: #f3f4f6;
  color: #374151;
}

.error-cancel-btn:hover {
  background: #e5e7eb;
  transform: translateY(-2px);
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, -50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 640px) {
  .error-container {
    width: 95%;
    padding: 16px;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
  }

  .error-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .error-icon {
    font-size: 28px;
  }

  .error-text h3 {
    font-size: 16px;
  }

  .error-actions {
    flex-direction: column;
  }

  .error-retry-btn,
  .error-cancel-btn {
    width: 100%;
  }
}

/* 暗色模式支持 */
@media (prefers-color-scheme: dark) {
  .error-container.error {
    background: rgba(239, 68, 68, 0.2);
  }

  .error-container.warning {
    background: rgba(245, 158, 11, 0.2);
  }

  .error-container.info {
    background: rgba(59, 130, 246, 0.2);
  }

  .error-container.success {
    background: rgba(16, 185, 129, 0.2);
  }

  .error-text h3 {
    color: #f3f4f6;
  }

  .error-text p {
    color: #d1d5db;
  }

  .error-details {
    background: rgba(255, 255, 255, 0.05);
  }

  .error-details pre {
    color: #e5e7eb;
  }

  .error-close-btn {
    color: #9ca3af;
  }

  .error-close-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #f3f4f6;
  }

  .error-cancel-btn {
    background: #374151;
    color: #f3f4f6;
  }

  .error-cancel-btn:hover {
    background: #4b5563;
  }
}
</style>
