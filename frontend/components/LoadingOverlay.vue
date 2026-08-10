<template>
  <transition name="fade">
    <div v-if="show" class="loading-overlay">
      <BlossomCanvas />
      <div class="flower-container">
        <div class="center-flower">🌸</div>
        <div
          v-for="petal in petals"
          :key="petal.id"
          class="petal"
          :style="petal.style"
        >
          🌸
        </div>
      </div>
      <div class="loading-text">稍等一下~ 春天正在加载中！</div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from "vue";
import BlossomCanvas from "./effects/BlossomCanvas.vue";

defineProps({
  show: {
    type: Boolean,
    default: false,
  },
});

const petals = computed(() => {
  const list = [];
  for (let i = 0; i < 6; i++) {
    const angle = (i / 6) * 360;
    const distance = 60 + Math.random() * 20;
    const size = 12 + Math.random() * 10;
    const duration = 3 + Math.random() * 2;
    const delay = Math.random() * 1.5;

    list.push({
      id: i,
      style: {
        "--angle": `${angle}deg`,
        "--distance": `${distance}px`,
        fontSize: `${size}px`,
        animationDuration: `${duration}s`,
        animationDelay: `${delay}s`,
      },
    });
  }
  return list;
});
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.flower-container {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.center-flower {
  position: absolute;
  font-size: 56px;
  z-index: 2;
  animation: pulse 2s ease-in-out infinite;
  filter: drop-shadow(0 0 10px rgba(255, 182, 193, 0.5));
}

.petal {
  position: absolute;
  animation: orbit var(--duration, 4s) linear infinite;
  animation-delay: var(--delay, 0s);
  opacity: 0.7;
}

.loading-text {
  margin-top: 20px;
  font-size: 18px;
  color: var(--color-text);
  text-shadow: 0 0 5px rgba(255, 182, 193, 0.5);
}

@keyframes orbit {
  from {
    transform: rotate(var(--angle, 0deg)) translateX(var(--distance, 60px))
      rotate(calc(-1 * var(--angle, 0deg)));
  }
  to {
    transform: rotate(calc(var(--angle, 0deg) + 360deg))
      translateX(var(--distance, 60px))
      rotate(calc(-1 * var(--angle, 0deg) - 360deg));
  }
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    filter: drop-shadow(0 0 10px rgba(255, 182, 193, 0.5));
  }
  50% {
    transform: scale(1.1);
    filter: drop-shadow(0 0 20px rgba(255, 182, 193, 0.8));
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
