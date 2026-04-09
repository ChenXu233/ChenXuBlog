<template>
  <div class="sunrise-wrapper">
    <!-- 太阳随着滚动向上升起，初始状态为 translateY(250px) 即底部被隐藏一半，产生"露出地平线"的效果 -->
    <div class="sunrise-effect" :style="{
      opacity: Math.max(0, 1 - progress * 3),
      transform: `translate(-50%,50%) scale(${1 + progress * 1})`
    }">
      <div class="sunrise-glow"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  progress: number;
}>();
</script>

<style scoped>
.sunrise-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 0;
}

.sunrise-effect {
  position: absolute;
  bottom: 0;
  left: 50%;
  transition: transform 0.1s ease-out, opacity 0.1s ease-out;
}

.sunrise-glow {
  width: 110vw;
  height: 110vw;
  border-radius: 50%;
  /* 柔和的晨曦散射：纯白核心 -> 浅暖黄 -> 淡香槟色 -> 融入空气的透明度 */
  background: radial-gradient(
    circle at 50% 50%,
    #ffffff 0%,
    #fff8e7 10%,
    #fce4b3 35%,
    rgba(252, 228, 179, 0.4) 60%,
    rgba(252, 228, 179, 0) 80%
  );
  filter: blur(12px);
  /* 柔和的晨光发光质感，去除刺眼的橘色 */
  box-shadow: 
    0 0 80px 15px rgba(255, 255, 255, 0.9),
    0 0 180px 50px rgba(252, 228, 179, 0.5);
}
</style>

