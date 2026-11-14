<template>
  <div class="elegant-home">
    <!-- Background Transition Layer (White to Bamboo Green) -->
    <div
      class="bg-transition-layer"
      :style="{ opacity: Math.min(1, scrollProgress * 1.5) }"
    ></div>

    <!-- Global Effects -->
    <BlossomCanvas />
    <RainCanvas />

    <!-- Section 1: Hero (Blossoms) -->
    <HomeHero :scroll-progress="scrollProgress" />

    <!-- Section 2: Progressive Introduction with Rain & Thunder -->
    <HomeZen />

    <!-- Bottom banner -->
    <section class="home-banner reveal-up v-observe">
      <div class="banner-inner">
        <div class="banner-bottom">
          <div class="banner-meta">
            <span>© 2026 ChenXuBlog. A blend of technology and blooming spring.</span>
            <a
              class="banner-icp"
              href="https://beian.miit.gov.cn/"
              target="_blank"
              rel="noopener"
              >浙ICP备2026024319号-1</a
            >
          </div>
          <span class="banner-mark">CHENXU / 2026</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";
import RainCanvas from "../components/effects/RainCanvas.vue";

// home 不套用 useSeo 的品牌后缀，标题保持独立；也避免从其它页面切换回来时残留旧标题
useHead({ title: "chenxu's homepage" });

const scrollProgress = ref(0);

let observer: IntersectionObserver | null = null;

// Intersection Observer for scroll reveal animations
const setupObserver = () => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-revealed");
        }
      });
    },
    { threshold: 0.15 },
  );

  const elements = document.querySelectorAll(".v-observe");
  elements.forEach((el) => observer?.observe(el));
};

// Global Scroll Progression & Effects
const handleScroll = () => {
  const progress = Math.min(window.scrollY / window.innerHeight, 1);
  scrollProgress.value = progress;

  // Fade out blossom and fade in rain based on scroll progress
  const blossomCanvas = document.getElementById("blossom-canvas");
  if (blossomCanvas) {
    blossomCanvas.style.opacity = Math.max(0, 1 - progress * 1.5).toString();
  }

  const rainCanvas = document.getElementById("rain-canvas");
  if (rainCanvas) {
    const rainOpacity = Math.max(0, Math.min(1, progress * 1.5 - 0.2));
    rainCanvas.style.opacity = rainOpacity.toString();
  }
};

onMounted(() => {
  setupObserver();
  handleScroll();
  document.body.classList.add("home-hide-scrollbar");

  // Initial rain opacity is 0 if at top of page
  const mainRain = document.getElementById("rain-canvas");
  if (mainRain && window.scrollY < window.innerHeight * 0.2) {
    mainRain.style.opacity = "0";
  }

  window.addEventListener("scroll", handleScroll, { passive: true });

  setTimeout(() => {
    document.querySelector(".hero-content")?.classList.add("is-revealed");
  }, 100);
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
  if (observer) observer.disconnect();
  document.body.classList.remove("home-hide-scrollbar");
});
</script>

<style scoped>
.elegant-home {
  color: #fff;
  font-family: "JetBrains Mono", monospace;
  /* clip both axes: the bamboo SVG draws past the page bottom and would create scroll space */
  overflow: clip;
  cursor: none; /* Hide default cursor */
  background: linear-gradient(to top, #fff9f0, #fff5e6);
  position: relative;
  z-index: 0;
}

.bg-transition-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #6a7664; /* Bamboo Green */
  z-index: -1;
  pointer-events: none;
}

.elegant-home a,
.elegant-home button,
.elegant-home .explore-btn,
.elegant-home :deep(.cyber-link) {
  cursor: none !important;
}

/* Animations (footer reveal) */
.reveal-up {
  opacity: 0;
  transform: translateY(40px);
  transition: all 1s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.is-revealed {
  opacity: 1 !important;
  transform: none !important;
  filter: blur(0) !important;
}

/* Bottom banner */
.home-banner {
  position: relative;
  z-index: 1;
  padding: 26px 0 24px;
  border-top: 3px solid #c07a6b;
  border-radius: 24px 24px 0 0;
  background: linear-gradient(180deg, #f7f3ea 0%, #f1ecdf 100%);
  color: #364036;
}

.banner-inner {
  width: min(1180px, calc(100% - 56px));
  margin: 0 auto;
}

.banner-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  font-size: 11px;
  color: #6d7569;
}

.banner-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.banner-icp {
  color: #8b9286;
  text-decoration: none;
  transition: color 0.2s ease;
}

.banner-icp:hover {
  color: #c07a6b;
}

.banner-mark {
  font-family: "JetBrains Mono", monospace;
  font-size: 9px;
  letter-spacing: 0.16em;
}

@media (max-width: 640px) {
  .home-banner {
    border-radius: 20px 20px 0 0;
    padding-bottom: 96px;
  }

  .banner-bottom {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}

</style>
