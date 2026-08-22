<template>
  <section class="hero-section">
    <!-- 初曦视差 -->
    <SunriseParallax :progress="scrollProgress" />

    <div class="hero-content reveal-blur" ref="heroText">
      <h1 class="elegant-title">
        <div class="title-line size-m">Amid April mists and</div>
        <div class="title-line size-x">bl🌸ss🌸ms</div>
        <div class="title-line size-s cn-title">烟花三月</div>
      </h1>
      <p class="hero-subtitle">
        晨煦的博客 · <span class="highlight-gold">诗与暖阳</span>
      </p>

      <div class="scroll-indicator">
        <div class="line-indicator"></div>
        <div class="line-indicator"></div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import SunriseParallax from "../effects/SunriseParallax.vue";

defineProps<{ scrollProgress: number }>();
</script>

<style scoped>
/* Animations (shared with sibling sections) */
.reveal-blur {
  opacity: 0;
  filter: blur(10px);
  transform: scale(0.95);
  transition: all 1.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.is-revealed {
  opacity: 1 !important;
  transform: none !important;
  filter: blur(0) !important;
}

.hero-section {
  background: transparent;
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  pointer-events: auto;
  margin-top: -10vh; /* Shift content slightly up */
}

.elegant-title {
  font-family: "Inter", "Helvetica Neue", "PingFang SC", sans-serif;
  line-height: 1.4;
  margin: 0;
  font-weight: 300;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.title-line {
  will-change: transform, opacity;
  color: #5a5a5a;
}
.size-x {
  font-size: 6rem;
  letter-spacing: -0.05em;
  opacity: 0.9;
  font-weight: 900;
}
.size-m {
  font-size: 4.5rem;
  letter-spacing: 0.05em;
  opacity: 0.9;
  font-weight: 900;
}

.size-s.cn-title {
  font-size: 2.5rem;
  letter-spacing: 0.3em;
  color: #c07a6b;
  opacity: 0.85;
  font-weight: 400;
}

.hero-subtitle {
  margin-top: 1.8rem;
  font-size: 2rem;
  letter-spacing: 0.2em;
  color: #8b9a7a;
  font-family: "Inter", "JetBrains Mono", sans-serif;
  font-weight: 800;
  opacity: 0.8;
}

.highlight-gold {
  color: #c9a87c;
}

.scroll-indicator {
  position: absolute;
  bottom: -40vh;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  opacity: 0.6;
  animation: pulseFade 2s infinite ease-in-out;
}

.line-indicator {
  width: 30px;
  height: 2px;
  background-color: #d4c5b0;
}

@keyframes pulseFade {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.8;
  }
}

@media (max-width: 768px) {
  .size-x {
    font-size: 3.5rem;
  }
  .size-m {
    font-size: 2.5rem;
  }
  .size-s.cn-title {
    font-size: 1.5rem;
  }
  .hero-subtitle {
    font-size: 1.2rem;
  }
}
</style>
