<template>
  <!-- Hardcore Cyber Stats Monitor -->
  <div class="cyber-monitor" :class="{ 'is-collapsed': isStatsCollapsed }">
    <div class="monitor-header" @click="isStatsCollapsed = !isStatsCollapsed">
      <span class="indicator"></span> SYS_MONITOR <span class="blink">_</span>
    </div>
    <div class="monitor-body">
      <div class="stat-row">
        <span>FPS</span><span class="stat-val">{{ currentFps }}</span>
      </div>
      <div class="stat-row">
        <span>MEM</span><span class="stat-val">{{ currentMem }} MB</span>
      </div>
      <div class="stat-row">
        <span>RES</span
        ><span class="stat-val">{{ winWidth }}x{{ winHeight }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";

const isStatsCollapsed = ref(false);
const currentFps = ref(0);
const currentMem = ref("0.00");
const winWidth = ref(window.innerWidth);
const winHeight = ref(window.innerHeight);

let statsAF = 0;
let frameCount = 0;
let lastTime = performance.now();

const updateStats = () => {
  const now = performance.now();
  frameCount++;
  if (now - lastTime >= 1000) {
    currentFps.value = Math.round((frameCount * 1000) / (now - lastTime));
    frameCount = 0;
    lastTime = now;

    // @ts-ignore
    if (performance.memory) {
      // @ts-ignore
      currentMem.value = (performance.memory.usedJSHeapSize / 1048576).toFixed(
        2,
      );
    }
  }
  winWidth.value = window.innerWidth;
  winHeight.value = window.innerHeight;
  statsAF = requestAnimationFrame(updateStats);
};

onMounted(() => {
  statsAF = requestAnimationFrame(updateStats);
});

onBeforeUnmount(() => {
  cancelAnimationFrame(statsAF);
});
</script>

<style scoped>
/* Hardcore Cyber Monitor Stats */
.cyber-monitor {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: rgba(5, 5, 10, 0.85);
  border: 1px solid #00f0ff;
  border-radius: 4px;
  padding: 10px;
  min-width: 140px;
  font-family: "JetBrains Mono", monospace;
  font-size: 0.85rem;
  color: #27c93f;
  z-index: 9999;
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
  backdrop-filter: blur(5px);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cyber-monitor.is-collapsed {
  transform: translateY(calc(100% - 30px));
}

.monitor-header {
  color: #00f0ff;
  font-size: 0.75rem;
  font-weight: bold;
  padding-bottom: 5px;
  border-bottom: 1px dashed rgba(0, 240, 255, 0.3);
  margin-bottom: 8px;
  cursor: pointer !important;
  display: flex;
  align-items: center;
  gap: 5px;
}

.indicator {
  width: 6px;
  height: 6px;
  background: #27c93f;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 5px #27c93f;
}

.blink {
  animation: blink-caret 1s step-end infinite;
}

@keyframes blink-caret {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

.stat-row {
  display: flex;
  justify-content: space-between;
  margin: 4px 0;
  pointer-events: none;
}

.stat-row span {
  opacity: 0.8;
}

.stat-val {
  color: #fff;
  opacity: 1 !important;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}
</style>
