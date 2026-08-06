<template>
  <div class="warm-window" :style="windowStyle" @mousedown="bringToFront">
    <!-- Window Header / Title Bar -->
    <div class="window-header" @mousedown.prevent="startDrag">
      <div class="window-title">
        <i v-if="app.icon" :class="['fa', app.icon, 'mr-2']"></i>
        {{ app.title }}
      </div>
      <div class="window-controls">
        <button
          class="control-btn minimize"
          @click.stop="$emit('minimize', app.id)"
        ></button>
        <button
          class="control-btn maximize"
          @click.stop="toggleMaximize"
        ></button>
        <button
          class="control-btn close"
          @click.stop="$emit('close', app.id)"
        ></button>
      </div>
    </div>

    <!-- Window Content -->
    <div class="window-content">
      <iframe
        v-if="app.type === 'iframe'"
        :src="app.url"
        class="window-iframe"
        frameborder="0"
      ></iframe>

      <component
        v-else-if="app.type === 'component'"
        :is="app.component"
        v-bind="app.props"
        class="window-vue-component"
      ></component>
    </div>

    <!-- Window Resizer Handles -->
    <div
      class="resize-handle left"
      @mousedown.prevent="startResize($event, 'left')"
    ></div>
    <div
      class="resize-handle top"
      @mousedown.prevent="startResize($event, 'top')"
    ></div>
    <div
      class="resize-handle right"
      @mousedown.prevent="startResize($event, 'right')"
    ></div>
    <div
      class="resize-handle bottom"
      @mousedown.prevent="startResize($event, 'bottom')"
    ></div>
    <div
      class="resize-handle bottom-left"
      @mousedown.prevent="startResize($event, 'bottomleft')"
    ></div>
    <div
      class="resize-handle bottom-right"
      @mousedown.prevent="startResize($event, 'bottomright')"
    ></div>
    <div
      class="resize-handle top-left"
      @mousedown.prevent="startResize($event, 'topleft')"
    ></div>
    <div
      class="resize-handle top-right"
      @mousedown.prevent="startResize($event, 'topright')"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from "vue";

const props = defineProps({
  app: {
    type: Object,
    required: true,
  },
  zIndex: {
    type: Number,
    default: 1,
  },
});

const emit = defineEmits(["close", "minimize", "focus"]);

// Window State
const isMaximized = ref(false);
const position = ref({
  x: props.app.defaultX || 100,
  y: props.app.defaultY || 100,
});
const size = ref({
  width: props.app.defaultWidth || 800,
  height: props.app.defaultHeight || 600,
});
const savedState = ref({ x: 0, y: 0, width: 0, height: 0 });

// Dragging State
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });

// Resizing State
const isResizing = ref(false);
const resizeDirection = ref("");
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0, posX: 0, posY: 0 });

const windowStyle = computed(() => {
  if (isMaximized.value) {
    return {
      top: "0px",
      left: "0px",
      width: "100%",
      height: "100%",
      zIndex: props.zIndex,
      transition:
        isDragging.value || isResizing.value ? "none" : "all 0.3s ease",
    };
  }
  return {
    top: `${position.value.y}px`,
    left: `${position.value.x}px`,
    width: `${size.value.width}px`,
    height: `${size.value.height}px`,
    zIndex: props.zIndex,
    transition: isDragging.value || isResizing.value ? "none" : "none",
  };
});

const bringToFront = () => {
  emit("focus", props.app.id);
};

const toggleMaximize = () => {
  if (isMaximized.value) {
    isMaximized.value = false;
    position.value.x = savedState.value.x;
    position.value.y = savedState.value.y;
    size.value.width = savedState.value.width;
    size.value.height = savedState.value.height;
  } else {
    savedState.value = {
      x: position.value.x,
      y: position.value.y,
      width: size.value.width,
      height: size.value.height,
    };
    isMaximized.value = true;
  }
};

// Drag logic
const startDrag = (e: MouseEvent) => {
  if (isMaximized.value) return;
  bringToFront();
  isDragging.value = true;
  dragOffset.value = {
    x: e.clientX - position.value.x,
    y: e.clientY - position.value.y,
  };
  document.addEventListener("mousemove", onDrag);
  document.addEventListener("mouseup", stopDrag);
};

const onDrag = (e: MouseEvent) => {
  if (!isDragging.value) return;
  position.value.x = e.clientX - dragOffset.value.x;
  position.value.y = Math.max(0, e.clientY - dragOffset.value.y); // Prevent dragging above screen
};

const stopDrag = () => {
  isDragging.value = false;
  document.removeEventListener("mousemove", onDrag);
  document.removeEventListener("mouseup", stopDrag);
};

// Resize logic
const startResize = (e: MouseEvent, dir: string) => {
  if (isMaximized.value) return;
  bringToFront();
  isResizing.value = true;
  resizeDirection.value = dir;
  resizeStart.value = {
    x: e.clientX,
    y: e.clientY,
    width: size.value.width,
    height: size.value.height,
    posX: position.value.x,
    posY: position.value.y,
  };

  // Create an overlay to prevent iframe stealing mouse events during resize
  const iframeOverlay = document.createElement("div");
  iframeOverlay.id = "resize-overlay";
  iframeOverlay.style.position = "fixed";
  iframeOverlay.style.top = "0";
  iframeOverlay.style.left = "0";
  iframeOverlay.style.right = "0";
  iframeOverlay.style.bottom = "0";
  iframeOverlay.style.zIndex = "9999";
  document.body.appendChild(iframeOverlay);

  document.addEventListener("mousemove", onResize);
  document.addEventListener("mouseup", stopResize);
};

const onResize = (e: MouseEvent) => {
  if (!isResizing.value) return;

  const dx = e.clientX - resizeStart.value.x;
  const dy = e.clientY - resizeStart.value.y;

  if (resizeDirection.value === "right") {
    size.value.width = Math.max(300, resizeStart.value.width + dx);
  }

  if (resizeDirection.value === "bottom") {
    size.value.height = Math.max(200, resizeStart.value.height + dy);
  }

  if (resizeDirection.value === "left") {
    const newWidth = Math.max(300, resizeStart.value.width - dx);
    if (newWidth !== size.value.width) {
      size.value.width = newWidth;
      position.value.x = resizeStart.value.posX + dx;
    }
  }

  if (resizeDirection.value === "top") {
    const newHeight = Math.max(200, resizeStart.value.height - dy);
    if (newHeight !== size.value.height) {
      size.value.height = newHeight;
      position.value.y = resizeStart.value.posY + dy;
    }
  }

  if (resizeDirection.value === "bottomleft") {
    const newWidth = Math.max(300, resizeStart.value.width - dx);
    const newHeight = Math.max(200, resizeStart.value.height + dy);
    if (newWidth !== size.value.width) {
      size.value.width = newWidth;
      position.value.x = resizeStart.value.posX + dx;
    }
    if (newHeight !== size.value.height) {
      size.value.height = newHeight;
    }
  }

  if (resizeDirection.value === "topleft") {
    const newWidth = Math.max(300, resizeStart.value.width - dx);
    const newHeight = Math.max(200, resizeStart.value.height - dy);
    if (newWidth !== size.value.width) {
      size.value.width = newWidth;
      position.value.x = resizeStart.value.posX + dx;
    }
    if (newHeight !== size.value.height) {
      size.value.height = newHeight;
      position.value.y = resizeStart.value.posY + dy;
    }
  }

  if (resizeDirection.value === "topright") {
    const newWidth = Math.max(300, resizeStart.value.width + dx);
    const newHeight = Math.max(200, resizeStart.value.height - dy);
    if (newWidth !== size.value.width) {
      size.value.width = newWidth;
    }
    if (newHeight !== size.value.height) {
      size.value.height = newHeight;
      position.value.y = resizeStart.value.posY + dy;
    }
  }

  if (resizeDirection.value === "bottomright") {
    const newWidth = Math.max(300, resizeStart.value.width + dx);
    const newHeight = Math.max(200, resizeStart.value.height + dy);
    if (newWidth !== size.value.width) {
      size.value.width = newWidth;
    }
    if (newHeight !== size.value.height) {
      size.value.height = newHeight;
    }
  }
};

const stopResize = () => {
  isResizing.value = false;
  const overlay = document.getElementById("resize-overlay");
  if (overlay) overlay.remove();
  document.removeEventListener("mousemove", onResize);
  document.removeEventListener("mouseup", stopResize);
};

onUnmounted(() => {
  document.removeEventListener("mousemove", onDrag);
  document.removeEventListener("mouseup", stopDrag);
  document.removeEventListener("mousemove", onResize);
  document.removeEventListener("mouseup", stopResize);
});
</script>

<style scoped>
.warm-window {
  position: absolute;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.window-header {
  height: 40px;
  background: rgba(255, 255, 255, 0.5);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px;
  user-select: none;
  cursor: grab;
}

.window-header:active {
  cursor: grabbing;
}

.window-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  display: flex;
  align-items: center;
}

.window-controls {
  display: flex;
  gap: 8px;
}

.control-btn {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: opacity 0.2s;
}

.control-btn:hover {
  opacity: 0.8;
}

.control-btn.close {
  background-color: #ff5f56;
}

.control-btn.minimize {
  background-color: #ffbd2e;
}

.control-btn.maximize {
  background-color: #27c93f;
}

.window-content {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #fff;
}

.window-iframe {
  width: 100%;
  height: 100%;
  display: block;
}

.window-vue-component {
  width: 100%;
  height: 100%;
  overflow: auto;
}

/* Resize Handles */
.resize-handle {
  position: absolute;
}
.resize-handle.left {
  top: 0;
  left: 0;
  width: 6px;
  height: 100%;
  cursor: ew-resize;
}
.resize-handle.top {
  top: 0;
  left: 0;
  width: 100%;
  height: 6px;
  cursor: ns-resize;
}
.resize-handle.right {
  top: 0;
  right: 0;
  width: 6px;
  height: 100%;
  cursor: ew-resize;
}
.resize-handle.bottom {
  bottom: 0;
  left: 0;
  width: 100%;
  height: 6px;
  cursor: ns-resize;
}
.resize-handle.bottom-right {
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  cursor: nwse-resize;
}
.resize-handle.bottom-left {
  bottom: 0;
  left: 0;
  width: 12px;
  height: 12px;
  cursor: nesw-resize;
}
.resize-handle.top-left {
  top: 0;
  left: 0;
  width: 12px;
  height: 12px;
  cursor: nwse-resize;
}
.resize-handle.top-right {
  top: 0;
  right: 0;
  width: 12px;
  height: 12px;
  cursor: nesw-resize;
}
</style>
