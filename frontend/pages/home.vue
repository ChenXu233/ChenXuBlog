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

    <!-- Footer -->
    <section class="footer-section">
      <div class="footer-note reveal-up v-observe">
        © 2026 ChenXuBlog. A blend of technology and blooming spring.
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";
import RainCanvas from "../components/effects/RainCanvas.vue";

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
  /* overflow-x: hidden causes position:sticky to break in scroll listeners, use clip */
  overflow-x: clip;
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

/* Footer */
.footer-section {
  padding: 1vh 5vw 5vh 10vw;
  background: #a8b7cb;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.footer-note {
  margin-top: 15vh;
  color: #444;
  font-size: 0.8rem;
  text-align: center;
  letter-spacing: 1px;
}
</style>
