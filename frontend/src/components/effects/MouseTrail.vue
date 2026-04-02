<template>
  <div>
    <!-- Custom Cursor -->
    <div
      ref="cursorRef"
      class="custom-cursor"
      :class="{ 'is-hover': isHovering }"
    >
      <span v-if="!isHovering" class="sakura">🌸</span>
      <svg
        v-else
        class="lightsaber"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <line
          x1="12"
          y1="0"
          x2="12"
          y2="24"
          stroke="#00f0ff"
          stroke-width="2"
        />
        <line
          x1="0"
          y1="12"
          x2="24"
          y2="12"
          stroke="#00f0ff"
          stroke-width="2"
        />
        <circle
          cx="12"
          cy="12"
          r="4"
          fill="#fff"
          stroke="#00f0ff"
          stroke-width="2"
        />
      </svg>
    </div>

    <!-- Trail Canvas -->
    <canvas ref="trailCanvasRef" id="trail-canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";

const cursorRef = ref<HTMLElement | null>(null);
const trailCanvasRef = ref<HTMLCanvasElement | null>(null);

let cursorX = 0;
let cursorY = 0;
const isHovering = ref(false);
let cursorRAF = 0;
let trailAnimationId: number;
const mouseTrail: { x: number; y: number; life: number }[] = [];

// ============ Custom Cursor ============

const handleCursorMove = (e: MouseEvent) => {
  cursorX = e.clientX;
  cursorY = e.clientY;

  const target = e.target as HTMLElement;
  if (
    target &&
    (target.tagName === "A" ||
      target.tagName === "BUTTON" ||
      target.closest("a") ||
      target.closest("button") ||
      target.closest(".explore-btn") ||
      target.closest(".cyber-link"))
  ) {
    isHovering.value = true;
  } else {
    isHovering.value = false;
  }
};

const updateCursor = () => {
  if (cursorRef.value) {
    cursorRef.value.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;
  }
  cursorRAF = requestAnimationFrame(updateCursor);
};

// ============ Trail Canvas ============

const handleMouseMoveTrail = (e: MouseEvent) => {
  const x = e.clientX;
  const y = e.clientY + window.scrollY;

  mouseTrail.push({ x, y, life: 1.0 });
  if (mouseTrail.length > 50) {
    mouseTrail.shift();
  }
};

const initTrailCanvas = () => {
  const canvas = trailCanvasRef.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const resizeCtx = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  window.addEventListener("resize", resizeCtx);
  resizeCtx();

  const drawTrail = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    if (mouseTrail.length > 0) {
      for (let i = 0; i < mouseTrail.length; i++) {
        const p = mouseTrail[i]!;
        p.life -= 0.05;
        if (p.life <= 0) continue;

        const renderY = p.y - window.scrollY;
        const isSakura = i % 2 === 0;

        ctx.beginPath();
        ctx.fillStyle = isSakura
          ? `rgba(255, 122, 162, ${p.life * 0.8})`
          : `rgba(0, 240, 255, ${p.life * 0.8})`;
        ctx.arc(p.x, renderY, p.life * 5, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    while (mouseTrail.length > 0 && mouseTrail[0]!.life <= 0) {
      mouseTrail.shift();
    }

    trailAnimationId = requestAnimationFrame(drawTrail);
  };
  drawTrail();
};

// ============ Lifecycle ============

onMounted(() => {
  window.addEventListener("mousemove", handleCursorMove);
  window.addEventListener("mousemove", handleMouseMoveTrail);
  updateCursor();
  initTrailCanvas();
});

onBeforeUnmount(() => {
  window.removeEventListener("mousemove", handleCursorMove);
  window.removeEventListener("mousemove", handleMouseMoveTrail);
  cancelAnimationFrame(cursorRAF);
  if (trailAnimationId) cancelAnimationFrame(trailAnimationId);
});
</script>

<style scoped>
/* Custom Cursor */
.custom-cursor {
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 10000;
  will-change: transform;
  margin-left: -12px;
  margin-top: -12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
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
    transform: scale(1.4) rotate(180deg);
    opacity: 1;
    filter: drop-shadow(0 0 8px rgba(255, 122, 162, 0.8));
  }
  100% {
    transform: scale(1) rotate(360deg);
    opacity: 0.8;
  }
}

.lightsaber {
  width: 24px;
  height: 24px;
  animation: pulse-lightsaber 1.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

@keyframes pulse-lightsaber {
  0%,
  100% {
    filter: drop-shadow(0 0 4px #00f0ff);
    transform: scale(1) rotate(0deg);
  }
  50% {
    filter: drop-shadow(0 0 10px #00f0ff);
    transform: scale(1.15) rotate(45deg);
  }
}

/* Trail Canvas */
#trail-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 9999;
}
</style>
