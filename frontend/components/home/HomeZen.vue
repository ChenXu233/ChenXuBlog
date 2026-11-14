<template>
  <section ref="rootEl" class="intro-section zen-canvas">
    <BambooParallax :progress="bambooProgress" />

    <div class="cx-container zen-container">
      <article class="profile-panel v-observe reveal-up">
        <div class="panel-main">
          <p class="handle cx-mono">ChenXu233</p>
          <h2 class="name">晨煦</h2>
          <p class="role">我是一位”全干工程师”。</p>
          <p class="bio">
            烟花三月，雾与花之间，我
            <span class="hl-soft">type</span> 了一行宇宙。
          </p>
        </div>

        <aside class="panel-side">
          <img
            class="avatar"
            :src="avatar"
            alt="晨煦的头像"
            width="120"
            height="120"
            @error="onAvatarError"
          />
        </aside>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import BambooParallax from "../effects/BambooParallax.vue";

const rootEl = ref<HTMLElement | null>(null);
const bambooProgress = ref(0);
const avatar = ref("https://avatars.githubusercontent.com/u/91937041?v=4&s=800");

function onAvatarError() {
  avatar.value = "/img/default-avatar.png";
}

function handleScroll() {
  if (!rootEl.value) return;
  const viewport = window.innerHeight;
  const rect = rootEl.value.getBoundingClientRect();
  bambooProgress.value = Math.max(
    0,
    Math.min(1, (viewport - rect.top) / viewport),
  );
}

onMounted(() => {
  handleScroll();
  window.addEventListener("scroll", handleScroll, { passive: true });
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
.reveal-up {
  opacity: 0;
  transform: translateY(34px);
  transition: all 1s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.is-revealed {
  opacity: 1 !important;
  transform: none !important;
}

.zen-canvas {
  position: relative;
  min-height: 70vh;
  display: flex;
  align-items: flex-start;
  padding: clamp(80px, 9vh, 130px) 0 clamp(56px, 8vw, 96px);
  background: transparent;
  color: #343a33;
  overflow: visible;
}

.zen-container {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
}

.profile-panel {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 0;
  align-items: stretch;
  width: min(960px, 100%);
  padding: 0;
  overflow: hidden;
  border-radius: 32px;
  border: 1px solid rgba(255, 255, 255, 0.55);
  background: linear-gradient(
    150deg,
    rgba(255, 255, 255, 0.85) 0%,
    rgba(255, 244, 238, 0.8) 46%,
    rgba(231, 243, 231, 0.76) 100%
  );
  backdrop-filter: blur(26px) saturate(1.1);
  -webkit-backdrop-filter: blur(26px) saturate(1.1);
  box-shadow:
    0 30px 80px -46px rgba(39, 48, 35, 0.55),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.panel-main {
  min-width: 0;
  padding: clamp(28px, 4vw, 52px);
}

.handle {
  margin: 0 0 12px;
  font-size: 11px;
  letter-spacing: 0.12em;
  color: #7b8377;
}

.name {
  margin: 0;
  font-family: "Inter", "PingFang SC", "Noto Sans SC", sans-serif;
  font-size: clamp(44px, 6vw, 68px);
  font-weight: 900;
  letter-spacing: -0.05em;
  line-height: 0.95;
  color: #2f352e;
}

.role {
  margin: 18px 0 0;
  font-size: 17px;
  font-weight: 700;
  color: #c07a6b;
}

.bio {
  margin: 14px 0 0;
  max-width: 34ch;
  font-size: 15px;
  line-height: 1.9;
  color: #4d564b;
}

.hl-soft {
  color: #c07a6b;
  font-weight: 700;
}

.panel-side {
  position: relative;
  min-height: 100%;
  height: 100%;
}

.avatar {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 0;
  object-fit: cover;
  background: rgba(255, 255, 255, 0.4);
}

@media (max-width: 760px) {
  .zen-canvas {
    min-height: 68vh;
    padding: 64px 0 56px;
  }

  .profile-panel {
    grid-template-columns: 1fr;
  }

  .panel-side {
    order: -1;
    aspect-ratio: 16 / 10;
    width: 100%;
    height: auto;
    min-height: 0;
  }

  .panel-main {
    padding: 26px 22px;
  }
}
</style>
