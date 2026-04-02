<template>
  <div class="elegant-home">
    <MouseTrail />
    <!-- Global Effects -->
    <BlossomCanvas />
    <RainCanvas />

    <!-- Section 1: Hero (Blossoms) -->
    <section class="hero-section">
      <div class="hero-content reveal-blur" ref="heroText">
        <h1 class="elegant-title">
          <div class="title-line size-m">Amid</div>
          <div class="title-line size-l">April mists</div>
          <div class="title-line size-s">and</div>
          <div class="title-line size-xl text-gradient alt">
            bl<span class="title-line text-gradient alt size-l raise">🌸</span
            >ss<span class="raise">🌸</span>ms
          </div>
        </h1>
        <p class="hero-subtitle">晨煦的个人空间 · 烟花三月，不必下扬州</p>

        <div class="scroll-indicator">
          <div class="mouse"></div>
          <span>SCROLL TO INITIATE</span>
        </div>
      </div>
    </section>

    <!-- Section 2: Progressive Introduction with Rain & Thunder -->
    <section class="intro-section" ref="introSection">
      <div class="intro-content-wrapper">
        <div class="glass-panel reveal-up v-observe full-width-panel">
          <h2 class="panel-title highlight-cyan">晨煦 / ChenXu233</h2>
          <p class="poetic-text">
            烟花三月，不必下扬州——<br />雾与花之间，我
            <span class="highlight-pink">type</span> 了一行宇宙。
          </p>
        </div>

        <div class="glass-panel reveal-up delay-1 v-observe right-align-panel">
          <h2 class="panel-title">👋 身份：全能干饭者</h2>
          <p>
            你好，我是晨煦，一名 <strong>全干开发者</strong>（全栈 +
            全能干饭）。<br /><br />
            <span class="tech-stack">> Rust · Python · TypeScript</span><br />
            从左到右分别是：性能、灵气、和让类型系统替我背锅。
          </p>
        </div>

        <div class="glass-panel reveal-up delay-2 v-observe">
          <h2 class="panel-title">🤖 赛博愿景</h2>
          <p>
            AI 爱好者，喜欢探索 <strong>软硬件协同的边界</strong>。<br /><br />
            我有一个不太小的野心：开发一门叫
            <span class="highlight-cyan">Type the Universe</span> 的语言 ——<br />让类型系统不仅约束变量，还能约束人生的不确定性<br />（虽然目前只约束了
            bug）。
          </p>
        </div>

        <div
          class="glass-panel reveal-up delay-1 v-observe full-width-panel center-align"
        >
          <h2 class="panel-title">🧠 思考小工厂</h2>
          <p>
            擅长领域：发呆 + 胡思乱想。这里是
            <strong>炫技 + 思考小工厂</strong>。你会看到：<br /><br />
          </p>
          <div class="bullet-list">
            <div class="bullet-item">// 奇奇怪怪的技术实验</div>
            <div class="bullet-item">// 软硬件结合的治愈翻车现场</div>
            <div class="bullet-item">
              // 以及一些发呆时想出来的、后来居然能跑的东西
            </div>
          </div>
          <p class="bottom-note">
            ☕ 如果你也喜欢在代码里藏一点浪漫，或者在焊电路板的时候泡一杯茶——<br />很高兴认识你。
          </p>
          <p class="social-links">
            📫 找到我：
            <a
              href="https://github.com/ChenXu233"
              target="_blank"
              class="cyber-link"
              >[GitHub · ChenXu233]</a
            >
          </p>
        </div>
      </div>
    </section>

    <!-- Section 3: Horizontal Scroll Module -->
    <section class="h-scroll-wrapper" ref="hScrollWrapper">
      <div class="h-scroll-sticky">
        <div class="h-scroll-track" ref="hScrollTrack">
          <!-- Card 1 -->
          <div class="h-scroll-panel">
            <div class="h-card">
              <div class="h-card-inner">
                <div class="h-card-front">
                  <div class="h-card-bg bg-1"></div>
                  <div class="h-card-content">
                    <span class="h-index">01</span>
                    <h2>ARTICLES <span class="cn-text">文章</span></h2>
                    <p>记录代码与灵感的灵光一现。</p>
                    <router-link to="/blog" class="explore-btn"
                      >Enter Module_</router-link
                    >
                  </div>
                </div>
                <div class="h-card-back">
                  <div class="debug-text">隐藏彩蛋 / DEBUG: Hello World</div>
                </div>
              </div>
            </div>
          </div>
          <!-- Card 2 -->
          <div class="h-scroll-panel">
            <div class="h-card">
              <div class="h-card-inner">
                <div class="h-card-front">
                  <div class="h-card-bg bg-2"></div>
                  <div class="h-card-content">
                    <span class="h-index">02</span>
                    <h2>ARCHIVE <span class="cn-text">归档</span></h2>
                    <p>时间轴上铭刻的所有过往与踪迹。</p>
                    <router-link to="/archive" class="explore-btn"
                      >Enter Module_</router-link
                    >
                  </div>
                </div>
                <div class="h-card-back">
                  <div class="debug-text">隐藏彩蛋 / DEBUG: Hello World</div>
                </div>
              </div>
            </div>
          </div>
          <!-- Card 3 -->
          <div class="h-scroll-panel">
            <div class="h-card">
              <div class="h-card-inner">
                <div class="h-card-front">
                  <div class="h-card-bg bg-3"></div>
                  <div class="h-card-content">
                    <span class="h-index">03</span>
                    <h2>LINKS <span class="cn-text">友链</span></h2>
                    <p>数字航海家的中转站与星图网路。</p>
                    <router-link to="/friend" class="explore-btn"
                      >Enter Module_</router-link
                    >
                  </div>
                </div>
                <div class="h-card-back">
                  <div class="debug-text">隐藏彩蛋 / DEBUG: Hello World</div>
                </div>
              </div>
            </div>
          </div>
          <!-- Card 4 -->
          <div class="h-scroll-panel">
            <div class="h-card">
              <div class="h-card-inner">
                <div class="h-card-front">
                  <div class="h-card-bg bg-4"></div>
                  <div class="h-card-content">
                    <span class="h-index">04</span>
                    <h2>DIARY <span class="cn-text">随谈</span></h2>
                    <p>抛开代码架构，回归纯粹的片语轻言。</p>
                    <router-link to="/diary" class="explore-btn"
                      >Enter Module_</router-link
                    >
                  </div>
                </div>
                <div class="h-card-back">
                  <div class="debug-text">隐藏彩蛋 / DEBUG: Hello World</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 4: Profile / User Module -->
    <section class="profile-section">
      <div class="profile-card reveal-blur v-observe">
        <div class="profile-header">
          <div class="dot red"></div>
          <div class="dot yellow"></div>
          <div class="dot green"></div>
          <span class="terminal-title">user_profile.sh</span>
        </div>
        <div class="profile-body">
          <div class="avatar-ring">
            <el-avatar
              src="https://avatars.githubusercontent.com/u/91937041?v=4"
              :size="120"
              class="avatar"
            />
          </div>
          <div class="profile-info">
            <h3>USER: <span class="highlight-pink">ADMIN / ChenXu</span></h3>
            <div class="typewriter-box">
              <p class="type-line">> System initialized.</p>
              <p class="type-line delay">
                > Core identity: Developer / Creator.
              </p>
              <p class="type-line delay-more">
                > Connection secure. Welcome back.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-note reveal-up v-observe">
        © 2026 ChenXuBlog. A blend of technology and blooming spring.
      </div>
    </section>

    <CyberMonitor />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";
import RainCanvas from "../components/effects/RainCanvas.vue";
import MouseTrail from "../components/effects/MouseTrail.vue";
import CyberMonitor from "../components/CyberMonitor.vue";

const titleLinesRef = ref<NodeListOf<HTMLElement> | null>(null);
const introSection = ref<HTMLElement | null>(null);
const introSectionHeight = ref<number | undefined>(undefined);

const hScrollWrapper = ref<HTMLElement | null>(null);
const hScrollTrack = ref<HTMLElement | null>(null);

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

  setTimeout(() => {
    if (introSection.value) {
      introSectionHeight.value = introSection.value.offsetHeight;
    }
  }, 300);

  window.addEventListener("resize", () => {
    if (introSection.value) {
      introSectionHeight.value = introSection.value.offsetHeight;
    }
  });
};

// Title 3D Parallax
const handleTitleParallax = () => {
  const scrollY = window.scrollY;
  const progress = Math.min(scrollY / window.innerHeight, 1);
  if (titleLinesRef.value) {
    titleLinesRef.value.forEach((line, index) => {
      const factor = (index + 1) * 40;
      const rotate = progress * factor;
      const translate = progress * factor * 1.5;
      line.style.transform = `rotateX(${rotate}deg) translateZ(${translate}px)`;
    });
  }

  // Fade subtitle and indicator
  const subtitle = document.querySelector(".hero-subtitle") as HTMLElement;
  if (subtitle) {
    subtitle.style.opacity = Math.max(0, 1 - progress * 2).toString();
    subtitle.style.transform = `translateY(${-progress * 150}px)`;
  }
  const scrollIndicator = document.querySelector(
    ".scroll-indicator",
  ) as HTMLElement;
  if (scrollIndicator) {
    scrollIndicator.style.opacity = Math.max(0, 1 - progress * 3).toString();
  }

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

// Horizontal Scroll Logic
const handleScroll = () => {
  if (!hScrollWrapper.value || !hScrollTrack.value) return;

  const rect = hScrollWrapper.value.getBoundingClientRect();
  const windowHeight = window.innerHeight;

  // Calculate progress of the scroll through the wrapper
  // When rect.top is 0, progress is 0.
  // When rect.top is -(rect.height - windowHeight), progress is 1.
  const maxScroll = rect.height - windowHeight;
  let progress = -rect.top / maxScroll;
  progress = Math.max(0, Math.min(1, progress));

  // 4 panels = 400vw width. Max translate needs to be exactly -(4 - 1) * 100vw = -300vw (or -75% of track width)
  // Using fixed percentage prevents scroll bugs
  hScrollTrack.value.style.transform = `translate3d(-${progress * 75}%, 0, 0)`;
};

onMounted(() => {
  setupObserver();

  // Initial rain opacity is 0 if at top of page
  const mainRain = document.getElementById("rain-canvas");
  if (mainRain && window.scrollY < window.innerHeight * 0.2) {
    mainRain.style.opacity = "0";
  }

  window.addEventListener("scroll", handleScroll, { passive: true });
  window.addEventListener("scroll", handleTitleParallax, { passive: true });

  // querySelectorAll returns a static NodeList, so it works fine here
  titleLinesRef.value = document.querySelectorAll(
    ".elegant-title .title-line",
  ) as NodeListOf<HTMLElement>;

  setTimeout(() => {
    document.querySelector(".hero-content")?.classList.add("is-revealed");
  }, 100);
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
  window.removeEventListener("scroll", handleTitleParallax);
  if (observer) observer.disconnect();
});
</script>

<style scoped>
/* Base Styles */
.elegant-home {
  background-color: #030305;
  color: #fff;
  font-family: "JetBrains Mono", monospace;
  /* overflow-x: hidden causes position:sticky to break in scroll listeners, use clip */
  overflow-x: clip;
  cursor: none; /* Hide default cursor */
}

.elegant-home a,
.elegant-home button,
.elegant-home .explore-btn,
.elegant-home .cyber-link {
  cursor: none !important;
}

/* Animations */
.reveal-up {
  opacity: 0;
  transform: translateY(40px);
  transition: all 1s cubic-bezier(0.2, 0.8, 0.2, 1);
}
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
.delay-1 {
  transition-delay: 0.2s;
}
.delay-2 {
  transition-delay: 0.4s;
}

/* Section 1: Hero */
.hero-section {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.mist-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, transparent 0%, #030305 100%);
  z-index: 2;
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 3;
  text-align: center;
  pointer-events: auto;
}

.elegant-title {
  perspective: 1500px;
  transform-style: preserve-3d;
  font-family: "aria", sans-serif;
  line-height: 1.1;
  margin: 0;
  font-weight: 1000;
  letter-spacing: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.title-line {
  transform-style: preserve-3d;
  will-change: transform;
  background: linear-gradient(120deg, #fff, #b2b2b2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.size-xl {
  font-size: 8rem;
  margin-top: -10px;
}
.size-l {
  font-size: 5rem;
}
.size-m {
  font-size: 3rem;
  opacity: 0.8;
}
.size-s {
  font-size: 2rem;
  opacity: 0.6;
  margin-top: -10px;
}

.text-gradient.alt {
  background: linear-gradient(120deg, #ff7aa2, #00f0ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  text-transform: lowercase;
}

.raise {
  display: inline-block;
  transform: translateY(-0.25em);
  vertical-align: middle;
}

.hero-subtitle {
  margin-top: 30px;
  font-size: 1.2rem;
  letter-spacing: 6px;
  color: #aaa;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.8);
}

.scroll-indicator {
  position: absolute;
  bottom: -12vh;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #666;
  font-size: 0.7rem;
  letter-spacing: 3px;
  opacity: 0.7;
}

.mouse {
  width: 20px;
  height: 35px;
  border: 2px solid #666;
  border-radius: 10px;
  margin-bottom: 10px;
  position: relative;
}

.mouse::before {
  content: "";
  position: absolute;
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #00f0ff;
  animation: scrollWheel 2s infinite;
}

@keyframes scrollWheel {
  0% {
    transform: translate(-50%, 0);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, 15px);
    opacity: 0;
  }
}

/* Section 2: Intro with Rain */
.intro-section {
  position: relative;
  padding: 15vh 0;
  background: transparent;
  z-index: 10;
  min-height: 100vh;
}

.intro-section.is-flashing::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.4);
  mix-blend-mode: overlay;
  pointer-events: none;
  z-index: 99;
  animation: flash-overlay 0.3s ease-out forwards;
}

@keyframes flash-overlay {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.intro-section.is-flashing .glass-panel {
  animation: panel-shake 0.3s ease-in-out;
}

@keyframes panel-shake {
  0%,
  100% {
    transform: translateY(0);
  }
  25% {
    transform: translate(2px, 2px);
  }
  50% {
    transform: translate(-2px, -2px);
  }
  75% {
    transform: translate(2px, -2px);
  }
}

.intro-content-wrapper {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 15vh;
  width: 80%;
  max-width: 1200px;
  margin: 0 auto;
}

.glass-panel {
  padding: 3rem 4rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.5),
    inset 0 0 20px rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(12px);
  border-left: 3px solid #ff7aa2;
  border-radius: 8px;
  color: #ddd;
  line-height: 1.8;
  width: 60%;
}

.right-align-panel {
  align-self: flex-end;
  border-left: none;
  border-right: 3px solid #00f0ff;
  text-align: right;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.01),
    rgba(0, 240, 255, 0.05)
  );
}

.full-width-panel {
  width: 100%;
  border-left: 3px solid rgba(255, 255, 255, 0.3);
}

.center-align {
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-top: 3px solid #ffbd2e;
}

.panel-title {
  font-family: "Cinzel", serif;
  color: #fff;
  font-size: 1.6rem;
  margin-bottom: 1.5rem;
  letter-spacing: 2px;
}

.poetic-text {
  font-size: 1.4rem;
  font-family: "Noto Serif SC", serif;
  line-height: 2.2;
}

.highlight-cyan {
  color: #00f0ff;
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
}
.highlight-pink {
  color: #ff7aa2;
  text-shadow: 0 0 10px rgba(255, 122, 162, 0.3);
  font-style: italic;
}

.tech-stack {
  font-family: "JetBrains Mono", monospace;
  color: #00f0ff;
  font-size: 1.1rem;
  background: rgba(0, 240, 255, 0.1);
  padding: 5px 15px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 5px;
}

.bullet-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
  font-size: 1.1rem;
  color: #bbb;
  margin-bottom: 2rem;
}

.bullet-item {
  position: relative;
}

.bottom-note {
  font-size: 1.1rem;
  color: #ddd;
  margin-bottom: 2rem;
}

.social-links {
  font-size: 1.2rem;
}

.cyber-link {
  color: #00f0ff;
  text-decoration: none;
  font-weight: 700;
  border-bottom: 1px dashed #00f0ff;
  transition: all 0.3s;
}

.cyber-link:hover {
  text-shadow: 0 0 10px #00f0ff;
  background: rgba(0, 240, 255, 0.1);
}

/* Section 3: Horizontal Scroll */
.h-scroll-wrapper {
  height: 400vh; /* 4 panels -> 400vh space */
  position: relative;
  background: #030305a2;
  backdrop-filter: blur(6px);
  z-index: 1;
}

.h-scroll-sticky {
  position: sticky;
  top: 0;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.h-scroll-track {
  display: flex;
  width: 400vw;
  height: 100%;
  will-change: transform;
}

.h-scroll-panel {
  width: 100vw;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 10vw;
  box-sizing: border-box;
}

.h-card {
  width: 100%;
  max-width: 900px;
  height: 60vh;
  position: relative;
  border-radius: 2px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 10px 50px rgba(0, 0, 0, 0.8);
  perspective: 1500px;
}

.h-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-style: preserve-3d;
}

.h-card:hover .h-card-inner {
  transform: rotateY(180deg);
}

.h-card-front,
.h-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 2px;
  overflow: hidden;
}

.h-card-back {
  transform: rotateY(180deg);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(10, 10, 15, 0.95);
  border: 1px dashed rgba(255, 122, 162, 0.3);
  box-shadow: inset 0 0 50px rgba(255, 122, 162, 0.05);
}

.debug-text {
  font-family: "JetBrains Mono", monospace;
  font-size: 1.5rem;
  color: #ff7aa2;
  text-shadow: 0 0 15px rgba(255, 122, 162, 0.4);
  letter-spacing: 2px;
}

.h-card-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  opacity: 0.3;
  transition:
    opacity 0.5s,
    transform 5s ease-out;
}

.h-card:hover .h-card-bg {
  opacity: 0.5;
  transform: scale(1.05);
}

.bg-1 {
  background-image: radial-gradient(
    circle at 80% 20%,
    rgba(255, 122, 162, 0.2),
    transparent
  );
}
.bg-2 {
  background-image: radial-gradient(
    circle at 20% 80%,
    rgba(0, 240, 255, 0.2),
    transparent
  );
}
.bg-3 {
  background-image: radial-gradient(
    circle at center,
    rgba(100, 50, 255, 0.2),
    transparent
  );
}
.bg-4 {
  background-image: radial-gradient(
    circle at 50% 0%,
    rgba(255, 200, 100, 0.2),
    transparent
  );
}

.h-card-content {
  position: relative;
  z-index: 2;
  padding: 4rem;
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.9) 0%,
    rgba(0, 0, 0, 0) 100%
  );
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.h-index {
  font-family: "Cinzel", serif;
  font-size: 5rem;
  color: rgba(255, 255, 255, 0.1);
  position: absolute;
  right: 5vh;
  top: 5vh;
  font-weight: bold;
}

.h-card-content h2 {
  font-size: 3.5rem;
  margin: 0 0 1rem 0;
  letter-spacing: 5px;
  font-family: "Cinzel", serif;
}

.cn-text {
  font-family: "JetBrains Mono", monospace;
  font-size: 1.5rem;
  color: #ff7aa2;
}

.h-card-content p {
  font-size: 1.2rem;
  color: #aaa;
  max-width: 60%;
  margin-bottom: 3rem;
  line-height: 1.8;
}

.explore-btn {
  align-self: flex-start;
  color: #00f0ff;
  text-decoration: none;
  font-size: 1.2rem;
  border-bottom: 2px solid transparent;
  padding-bottom: 5px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 10px;
}

.explore-btn::after {
  content: "→";
  transition: transform 0.3s;
}

.explore-btn:hover {
  border-color: #00f0ff;
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
}

.explore-btn:hover::after {
  transform: translateX(10px);
}

/* Section 4: Profile */
.profile-section {
  padding: 20vh 10vw 10vh 10vw;
  background: #030305;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.profile-card {
  width: 100%;
  max-width: 700px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(20, 20, 25, 0.8);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}

.profile-header {
  background: rgba(0, 0, 0, 0.5);
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
.dot.red {
  background: #ff5f56;
}
.dot.yellow {
  background: #ffbd2e;
}
.dot.green {
  background: #27c93f;
}

.terminal-title {
  margin-left: 10px;
  color: #666;
  font-size: 0.9rem;
}

.profile-body {
  padding: 40px;
  display: flex;
  gap: 40px;
  align-items: center;
}

.avatar-ring {
  padding: 5px;
  border: 2px dashed rgba(255, 122, 162, 0.5);
  border-radius: 50%;
  animation: spin 20s linear infinite;
}

.avatar {
  border-radius: 50%;
  display: block;
  animation: spin 20s linear infinite reverse;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

.profile-info h3 {
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  letter-spacing: 2px;
}

.typewriter-box {
  background: rgba(0, 0, 0, 0.6);
  padding: 20px;
  border-radius: 4px;
  border-left: 2px solid #00f0ff;
}

.type-line {
  margin: 5px 0;
  color: #88b0b0;
  overflow: hidden;
  white-space: nowrap;
  font-size: 0.9rem;
}

.footer-note {
  margin-top: 15vh;
  color: #444;
  font-size: 0.8rem;
  text-align: center;
  letter-spacing: 1px;
}

/* Responsive */
@media (max-width: 1024px) {
  .size-xl {
    font-size: 4rem;
  }
  .size-l {
    font-size: 3rem;
  }
  .size-m {
    font-size: 2rem;
  }
  .glass-panel {
    width: 90%;
    padding: 2rem;
  }
  .h-scroll-panel {
    padding: 0 5vw;
  }
  .h-card-content {
    padding: 2rem;
    background: rgba(0, 0, 0, 0.6);
  }
  .h-card-content p {
    max-width: 100%;
  }
  .profile-body {
    flex-direction: column;
    text-align: center;
  }
}
</style>
