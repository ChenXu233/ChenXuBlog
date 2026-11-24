<template>
  <section ref="rootEl" class="intro-section zen-canvas">
    <BambooParallax :progress="bambooProgress" />

    <div class="cx-container zen-container">
      <article class="profile-panel v-observe reveal-up">
        <div class="panel-main">
          <p class="handle cx-mono">ChenXu233</p>
          <h2 class="name">晨煦</h2>
          <p class="role">是一位“全干工程师”。</p>
          <div class="bio">
            <p>目前攻读本科光电信息科学与工程，是计算机狂热者。</p>
            <p>
              主要兴趣在于全栈开发/人工智能技术，拥有一些开源项目经验，当前正在学习
              CPU 架构/编译原理/单片机。
            </p>
            <p>主要使用语言：中文（母语），英语。</p>
            <p>
              主要使用编程语言：Python、JavaScript/TypeScript、Go、Rust、Kotlin
              等。
            </p>
            <p>
              邮箱：<a class="hl-soft" href="mailto:Woyerpa@outlook.com"
                >Woyerpa@outlook.com</a
              >
            </p>
          </div>
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

      <div class="more-wrap v-observe reveal-up">
        <NuxtLink to="/article" class="more-link">
          查看更多文章
          <i class="fa fa-long-arrow-right" aria-hidden="true"></i>
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import BambooParallax from "../effects/BambooParallax.vue";

const rootEl = ref<HTMLElement | null>(null);
const bambooProgress = ref(0);
const avatar = ref(
  "https://avatars.githubusercontent.com/u/91937041?v=4&s=800",
);

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
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(24px, 3vw, 40px);
}

.more-wrap {
  display: flex;
  justify-content: center;
}

.more-link {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 14px 28px;
  border-radius: 999px;
  background: #c07a6b;
  color: #fff8f2;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.04em;
  box-shadow: 0 16px 34px -22px rgba(120, 60, 45, 0.9);
  transition:
    transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1),
    background-color 0.25s ease,
    box-shadow 0.25s ease;
}

.more-link i {
  transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.more-link:hover {
  background: #b06a5c;
  transform: translateY(-2px);
  box-shadow: 0 20px 40px -22px rgba(120, 60, 45, 0.95);
}

.more-link:hover i {
  transform: translateX(4px);
}

.profile-panel {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 0;
  align-items: stretch;
  /* 最宽 70vw，且不超过容器的 90%，最窄 300px */
  width: clamp(300px, 70vw, 90%);
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
  padding: clamp(28px, 3vw, 52px);
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
  max-width: 38ch;
  font-size: 15px;
  line-height: 1.9;
  color: #4d564b;
}

/* HTML 会把源码换行折成空格，所以每条信息单独成段 */
.bio p {
  margin: 0 0 10px;
}

.bio p:last-child {
  margin-bottom: 0;
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
