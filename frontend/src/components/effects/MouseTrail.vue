<template>
  <div class="cursor-container">
    <div
      class="cursor-dot"
      :class="{ 'is-hidden': isHovering }"
      :style="{ transform: `translate3d(${mouseX}px, ${mouseY}px, 0)` }"
    >
      <span class="sakura">🌸</span>
    </div>

    <div
      class="cursor-ring"
      :class="{ 'is-magnetic': isHovering }"
      :style="{
        transform: `translate3d(${ringX}px, ${ringY}px, 0)`,
        width: `${ringW}px`,
        height: `${ringH}px`,
        borderRadius: ringRadius,
      }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";

const mouseX = ref(-100);
const mouseY = ref(-100);

const ringX = ref(-100);
const ringY = ref(-100);
const ringW = ref(40);
const ringH = ref(40);
const ringRadius = ref("50%");

const isHovering = ref(false);

let targetRingX = -100;
let targetRingY = -100;
let targetRingW = 40;
let targetRingH = 40;
let targetRadius = "50%";

let rafId = 0;

const handleMouseMove = (e: MouseEvent) => {
  mouseX.value = e.clientX;
  mouseY.value = e.clientY;

  const target = e.target as HTMLElement;
  const clickable = target.closest(
    'a, button, input, .cursor-pointer, .glass-panel, [role="button"]',
  );

  if (clickable) {
    isHovering.value = true;
    const rect = clickable.getBoundingClientRect();

    const padding = 8;

    targetRingW = rect.width + padding * 2;
    targetRingH = rect.height + padding * 2;
    targetRingX = rect.left - padding;
    targetRingY = rect.top - padding;

    const style = window.getComputedStyle(clickable);
    if (style.borderRadius && style.borderRadius !== "0px") {
      targetRadius = style.borderRadius;
    } else {
      targetRadius = "12px";
    }
  } else {
    isHovering.value = false;

    targetRingW = 40;
    targetRingH = 40;
    targetRingX = mouseX.value - targetRingW / 2;
    targetRingY = mouseY.value - targetRingH / 2;
    targetRadius = "50%";
  }
};

const updatePhysics = () => {
  if (!isHovering.value) {
    targetRingX = mouseX.value - targetRingW / 2;
    targetRingY = mouseY.value - targetRingH / 2;
  }

  ringX.value += (targetRingX - ringX.value) * 0.15;
  ringY.value += (targetRingY - ringY.value) * 0.15;
  ringW.value += (targetRingW - ringW.value) * 0.15;
  ringH.value += (targetRingH - ringH.value) * 0.15;

  if (ringRadius.value !== targetRadius) {
    ringRadius.value = targetRadius;
  }

  rafId = requestAnimationFrame(updatePhysics);
};

onMounted(() => {
  window.addEventListener("mousemove", handleMouseMove);
  rafId = requestAnimationFrame(updatePhysics);
});

onBeforeUnmount(() => {
  window.removeEventListener("mousemove", handleMouseMove);
  if (rafId) cancelAnimationFrame(rafId);
});
</script>

<style scoped>
.cursor-container {
  pointer-events: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 10000;
  overflow: visible; /* 改为 visible 防止容器拦截事件 */
}

.cursor-dot {
  position: absolute;
  top: 0;
  left: 0;
  background-color: transparent;
  pointer-events: none;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: -12px;
  margin-top: -12px;
  width: 24px;
  height: 24px;
}

.cursor-container * {
  pointer-events: none !important;
}

.sakura {
  font-size: 24px;
  line-height: 1;
  transform-origin: center;
  animation: breathe-sakura 4s linear infinite;
  display: inline-block;
}

@keyframes breathe-sakura {
  0% {
    transform: scale(1) rotate(0deg);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2) rotate(180deg);
    opacity: 1;
    filter: drop-shadow(0 0 8px rgba(255, 122, 162, 0.8))
      drop-shadow(0 0 16px rgba(0, 212, 255, 0.5));
  }
  100% {
    transform: scale(1) rotate(360deg);
    opacity: 0.8;
  }
}

.cursor-dot.is-hidden {
  opacity: 0.1;
  transform: scale(0.5);
}

.cursor-ring {
  position: absolute;
  top: 0;
  left: 0;
  border: 1px solid var(--color-primary-light);
  box-shadow: 0 0 12px var(--color-primary-light);
  pointer-events: none;

  transition:
    border-radius 0.3s cubic-bezier(0.23, 1, 0.32, 1),
    background-color 0.3s ease,
    backdrop-filter 0.3s ease,
    border-color 0.3s ease;

  will-change: width, height, transform, border-radius;
}

.cursor-ring.is-magnetic {
  border-color: var(--color-primary);
}
</style>
