<template>
  <div class="site-shell" :class="{ 'lock-light': isHome }">
    <a class="skip-link" href="#main">跳到正文</a>
    <div v-if="!isHome" class="site-bg" aria-hidden="true"></div>
    <main id="main" class="site-main">
      <slot />
    </main>
    <SiteFooter v-if="!isHome" />
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const isHome = computed(() => route.path === "/home");
</script>

<style scoped>
.site-shell {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.site-main {
  flex: 1;
  width: 100%;
}

/* home keeps its original warm scene, even in dark mode */
.lock-light {
  color-scheme: light;
  --cx-paper: #f3f0e8;
  --cx-paper-deep: #eae5d9;
  --cx-surface: #fffdf7;
  --cx-surface-rgb: 255, 253, 247;
  --cx-glass-a: 255, 253, 248;
  --cx-glass-b: 252, 251, 247;
  --cx-ink: #14120f;
  --cx-ink-soft: #514c43;
  --cx-ink-mute: #7d776c;
  --cx-line: rgba(20, 18, 15, 0.12);
  --cx-line-strong: rgba(20, 18, 15, 0.26);
  --cx-shadow: 0 30px 80px -44px rgba(20, 18, 15, 0.45);
}

.skip-link {
  position: fixed;
  top: 8px;
  left: 8px;
  z-index: 200;
  padding: 10px 16px;
  border-radius: 10px;
  background: var(--cx-accent);
  color: var(--cx-accent-ink);
  font-family: var(--cx-font-mono);
  font-size: 11px;
  transform: translateY(-160%);
  transition: transform 0.2s ease;
}

.skip-link:focus {
  transform: translateY(0);
}
</style>
