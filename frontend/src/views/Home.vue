<template>
  <div class="elegant-home">
    <MouseTrail />
    <!-- Global Effects -->
    <BlossomCanvas />
    <RainCanvas />

    <!-- Section 1: Hero (Blossoms) -->
    <section class="hero-section">
      <div class="mist-overlay"></div>
      <div class="hero-content reveal-blur" ref="heroText">
        <h1 class="elegant-title">
          <div class="title-line size-m">Amid</div>
          <div class="title-line size-l">April mists</div>
          <div class="title-line size-s">and</div>
          <div class="title-line size-xl text-gradient alt">
            bl<span class="title-line text-gradient alt size-l">🌸</span>ss<span
              class=""
              >🌸</span
            >ms
          </div>
        </h1>
        <p class="hero-subtitle">晨煦的个人空间 · 烟花三月</p>

        <div class="scroll-indicator">
          <div class="mouse"></div>
          <span>SCROLL TO INITIATE</span>
        </div>
      </div>
    </section>

    <!-- Section 2: Progressive Introduction with Rain & Thunder -->
    <section class="intro-section zen-canvas" ref="introSection">
      <div class="zen-watermark v-observe fade-in-scroll">C.X_UNIVERSE</div>

      <div class="zen-container">
        <!-- 板块一：开门见山 -->
        <div class="zen-block block-intro v-observe reveal-up">
          <div class="zen-hero-name">
            <span>晨</span>
            <span>煦</span>
          </div>
          <div class="zen-biography">
            <div class="zen-subtitle">ChenXu233 // SYS.ADMIN</div>
            <div class="zen-prose">
              烟花三月，雾与花之间，我
              <span class="hl-soft">type</span> 了一行宇宙。
            </div>
            <div class="zen-quote">
              “发呆不是浪费生命，是给生命留出编译的时间。”
            </div>
          </div>
        </div>

        <!-- 板块二：日常状态（Orbiting Avatar & Capsules） -->
        <div class="zen-block block-status v-observe reveal-up delay-1">
          <div class="status-text">
            <h3>别人叫我“全干工程师”。不是全栈，是全都干——</h3>
            <p>写代码、聊哲学、推物理、焊电路、发呆、胡思乱想、吃白饭。</p>
            <p class="status-summary">
              发呆是我最强的 debug 工具，<br />
              吃白饭是我最低成本的快乐，<br />
              至于哲学和物理——反正宇宙也没说我不能想。
            </p>
          </div>

          <div class="zen-avatar-system">
            <div class="enso-circle"></div>
            <el-avatar
              src="https://avatars.githubusercontent.com/u/91937041?v=4"
              :size="120"
              class="zen-avatar-core"
            />
            <!-- 横版胶囊状态小组件 -->
            <div class="z-capsule cap-1">
              <span class="c-emoji">🍚</span>
              <div class="c-details">
                <strong>吃白饭</strong><span>米饭是碳水，也是灵感燃料</span>
              </div>
            </div>
            <div class="z-capsule cap-2">
              <span class="c-emoji">⌨️</span>
              <div class="c-details">
                <strong>写代码</strong><span>Rust底层 / Py脚本 / TS诗</span>
              </div>
            </div>
            <div class="z-capsule cap-3">
              <span class="c-emoji">🪐</span>
              <div class="c-details">
                <strong>聊哲学</strong><span>bug存不存在于未观测</span>
              </div>
            </div>
            <div class="z-capsule cap-4">
              <span class="c-emoji">📐</span>
              <div class="c-details">
                <strong>推物理</strong><span>从欧姆定律到量子力学</span>
              </div>
            </div>
            <div class="z-capsule cap-5">
              <span class="c-emoji">😶‍🌫️</span>
              <div class="c-details">
                <strong>发呆</strong><span>发呆才是核心生产力</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 板块三：技术野心 (Floating Windows 巧思) -->
        <div class="zen-block block-ambition v-observe reveal-up delay-2">
          <div class="ambition-header">探 索 边 界 // EXPLORATION</div>
          <div class="floating-grid">
            <div class="float-window win-glass">
              <div class="win-dot red"></div>
              <div class="win-dot yellow"></div>
              <div class="win-dot green"></div>
              <h4>[ YaoXiang ]</h4>
              <p>
                愿景：<strong>Type the Universe</strong>。<br />
                欢迎来点 star，或者点 issue 骂我。<br />
                <a
                  href="https://github.com/ChenXu233/YaoXiang"
                  target="_blank"
                  class="cyber-link"
                  >ChenXu233/YaoXiang ↗</a
                >
              </p>
            </div>

            <div class="float-window win-cyber">
              <div class="win-status">System.IO.Hardware</div>
              <h4>软硬协同</h4>
              <p>
                深入学习计算机组成原理，希望有一天能为“多核原生”做出自己的贡献，让软件和硬件不再互相甩锅。
              </p>
            </div>

            <div class="float-window win-agape">
              <div class="win-icon">⚙️</div>
              <h4>AGI 执念</h4>
              <p>听起来很中二但我是认真的：<br />实现能改变世界的 AGI。</p>
            </div>

            <div class="float-window win-neuro">
              <div class="win-header">
                <strong>脑电 + MR</strong>
                <span class="win-badge">进度: 60%准率</span>
              </div>
              <p>
                发个呆，光标就动了；想个类型，代码就生成了。<br />
                目前能分辨“我在发呆”和“认真想bug”的区别。
              </p>
            </div>
          </div>
          <p class="ambition-footer">
            对类型系统、计组、AGI、脑机接口感兴趣？欢迎脑暴。<strong
              >发呆小广告位常年招租。</strong
            >
          </p>
        </div>

        <!-- 板块四：小工厂出品 + 联系方式 -->
        <div class="zen-block block-factory v-observe reveal-up delay-3">
          <div class="factory-split">
            <div class="f-left">
              <h4>炫技 + 思考小工厂</h4>
              <ul class="f-list">
                <li>
                  <strong>奇奇怪怪的实验</strong>：用 TS 写会发朋友圈的机器人
                </li>
                <li>
                  <strong>软硬结合翻车现场</strong>：焊电路板烫到手，但 LED
                  居然亮了
                </li>
                <li><strong>发呆产物</strong>：用 Python 远程控制家里花洒</li>
                <li><strong>瞎折腾记录</strong>：从“脑控小灯”到“脑控 IDE”</li>
                <li>
                  <strong>写写诗</strong>：代码诗与文字诗，质量随发呆时长波动
                </li>
              </ul>
            </div>
            <div class="f-right">
              <div class="contact-box">
                <div class="c-greeting">
                  如果你也喜欢在代码里藏一点浪漫，<br />或者在焊电路板的时候泡一杯茶——很高兴认识你。
                </div>
                <div class="c-joke">
                  > 发呆时长 > 10,000 hrs<br />
                  > 发呆领域资深专家<br />
                  > 可接发呆咨询（收费：一杯奶茶）
                </div>
                <div class="c-links">
                  <a
                    href="https://github.com/ChenXu233"
                    target="_blank"
                    class="c-btn"
                    ><i class="icon">G</i> GitHub</a
                  >
                  <a href="#" class="c-btn"
                    ><i class="icon">R</i> 小红书·晨煦发呆中</a
                  >
                  <a href="mailto:chenxu233@type.universe" class="c-btn"
                    ><i class="icon">M</i> chenxu233@type.universe</a
                  >
                </div>
              </div>
            </div>
          </div>
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <section class="footer-section">
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
  background: #030305;
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
  background-image: url("../assets/sukra.jpg");
  background-size: auto 100vw;
  background-position: center;
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
  background: #030305cc;
  backdrop-filter: blur(10px);
  z-index: 0;
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
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

/* Section 2: Soft Zen Canvas */
.zen-canvas {
  position: relative;
  width: 100vw;
  min-height: 100vh;
  margin-left: calc(-50vw + 50%);
  padding: 8rem 0;
  display: flex;
  justify-content: center;
  background: #030305;
  font-family: "PingFang SC", "Noto Sans SC", sans-serif;
  color: #e2e8f0;
  overflow: hidden;
}

.zen-watermark {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 15vw;
  font-family: "JetBrains Mono", monospace;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.015);
  letter-spacing: -2px;
  pointer-events: none;
  z-index: 0;
  white-space: nowrap;
}

.zen-block {
  z-index: 2;
  backdrop-filter: blur(10px);
}

.zen-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1200px;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 8rem;
}

/* BLOCK 1: INTRO */
.block-intro {
  display: flex;
  align-items: center;
  gap: 4rem;
}
.zen-hero-name {
  display: flex;
  flex-direction: column;
  font-size: 4.5rem;
  font-weight: 200;
  letter-spacing: 0.5rem;
  color: #fff;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding-right: 3rem;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}
.zen-biography {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.zen-subtitle {
  font-family: "JetBrains Mono", monospace;
  color: rgba(255, 255, 255, 0.4);
  font-size: 1rem;
  letter-spacing: 2px;
}
.zen-prose {
  font-size: 1.8rem;
  font-weight: 300;
  line-height: 1.6;
}
.hl-soft {
  color: #f4b3c2;
  font-style: italic;
  font-family: "JetBrains Mono", monospace;
  font-weight: bold;
}
.zen-quote {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.6);
  border-left: 2px solid rgba(255, 255, 255, 0.2);
  padding-left: 1rem;
  font-style: italic;
}

/* BLOCK 2: STATUS & ORBIT AVATAR */
.block-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 24px;
  padding: 4rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}
.status-text {
  flex: 1;
  max-width: 500px;
}
.status-text h3 {
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 2rem;
  color: #f4b3c2;
}
.status-text p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.8;
  margin-bottom: 1.5rem;
}
.status-summary {
  background: rgba(0, 0, 0, 0.3);
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 3px solid rgba(244, 179, 194, 0.4);
  font-size: 1rem !important;
}

.zen-avatar-system {
  position: relative;
  width: 400px;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.enso-circle {
  position: absolute;
  width: 250px;
  height: 250px;
  border-radius: 50%;
  border: 1px dashed rgba(255, 255, 255, 0.1);
  animation: slow-spin 40s linear infinite;
}
.enso-circle::before {
  content: "";
  position: absolute;
  top: -2px;
  left: 50%;
  width: 5px;
  height: 5px;
  background: #f4b3c2;
  border-radius: 50%;
  box-shadow: 0 0 10px #f4b3c2;
}

/* CAPSULE (Horizontal) WIDGETS */
.z-capsule {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: rgba(20, 22, 28, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 0.6rem 1.2rem 0.6rem 0.6rem;
  border-radius: 50px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  white-space: nowrap;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}
.z-capsule:hover {
  transform: scale(1.05) translateY(-5px);
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
  z-index: 10;
}
.c-emoji {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  font-size: 1.2rem;
}
.c-details {
  display: flex;
  flex-direction: column;
}
.c-details strong {
  font-weight: 500;
  font-size: 0.95rem;
  color: #fff;
  letter-spacing: 1px;
}
.c-details span {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
}

/* Orbit Positioning - Elliptical style around avatar */
.cap-1 {
  top: 5%;
  left: 0%;
  transform: rotate(-5deg);
}
.cap-2 {
  top: 25%;
  right: -15%;
  transform: rotate(3deg);
}
.cap-3 {
  bottom: 20%;
  right: -10%;
  transform: rotate(-2deg);
}
.cap-4 {
  bottom: -5%;
  left: 10%;
  transform: rotate(4deg);
}
.cap-5 {
  bottom: 35%;
  left: -25%;
  transform: rotate(-4deg);
}

.cap-1:hover,
.cap-2:hover,
.cap-3:hover,
.cap-4:hover,
.cap-5:hover {
  transform: scale(1.05) translateY(-5px) rotate(0deg);
}

/* BLOCK 3: AMBITION */
.block-ambition {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}
.ambition-header {
  font-size: 1rem;
  letter-spacing: 4px;
  color: rgba(255, 255, 255, 0.3);
  text-align: center;
  font-family: "JetBrains Mono", monospace;
}
.floating-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  position: relative;
}
.float-window {
  background: rgba(25, 28, 36, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 2.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.float-window:hover {
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
  background: rgba(30, 33, 42, 0.6);
}
.float-window h4 {
  font-size: 1.4rem;
  font-weight: 500;
  color: #f4b3c2;
  margin-bottom: 1.2rem;
}
.float-window p {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.65);
  line-height: 1.8;
}

/* 浮窗巧思设计 */
.win-glass {
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.06) 0%,
    rgba(255, 255, 255, 0) 100%
  );
}
.win-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 6px;
  margin-bottom: 1.5rem;
}
.win-dot.red {
  background: #ff5f56;
}
.win-dot.yellow {
  background: #ffbd2e;
}
.win-dot.green {
  background: #27c93f;
}

.win-cyber .win-status {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.8rem;
  color: #4ade80;
  margin-bottom: 1rem;
  opacity: 0.8;
  border-bottom: 1px solid rgba(74, 222, 128, 0.2);
  display: inline-block;
  padding-bottom: 4px;
}

.win-agape {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.win-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.win-neuro .win-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}
.win-neuro h4 {
  margin-bottom: 0;
}
.win-badge {
  background: rgba(244, 179, 194, 0.15);
  color: #f4b3c2;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  border: 1px solid rgba(244, 179, 194, 0.3);
}

.cyber-link {
  display: inline-block;
  margin-top: 1.5rem;
  color: #fff;
  font-family: "JetBrains Mono", monospace;
  text-decoration: none;
  font-size: 0.9rem;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.4);
  transition: all 0.2s;
}
.cyber-link:hover {
  color: #f4b3c2;
  border-color: #f4b3c2;
}
.ambition-footer {
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.1rem;
  margin-top: 1rem;
}

/* BLOCK 4: FACTORY & CONTACT */
.factory-split {
  display: flex;
  background: rgba(17, 19, 26, 0.6);
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}
.f-left {
  flex: 55%;
  padding: 4rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), transparent);
}
.f-left h4 {
  font-size: 1.6rem;
  font-weight: 400;
  margin-bottom: 2rem;
  color: #e2e8f0;
}
.f-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.f-list li {
  position: relative;
  padding-left: 2rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
}
.f-list li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #f4b3c2;
  font-family: monospace;
}
.f-list strong {
  color: #e2e8f0;
  font-weight: 500;
}

.f-right {
  flex: 45%;
  padding: 4rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
  border-left: 1px solid rgba(255, 255, 255, 0.02);
}
.c-greeting {
  font-size: 1.1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
  font-style: italic;
}
.c-joke {
  background: rgba(255, 255, 255, 0.03);
  padding: 1.5rem;
  border-radius: 12px;
  font-family: "JetBrains Mono", monospace;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.8;
  margin-bottom: 2.5rem;
  border-left: 2px solid rgba(255, 255, 255, 0.1);
}
.c-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.c-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  color: #e2e8f0;
  text-decoration: none;
  transition: all 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.c-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateX(5px);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}
.c-btn .icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 28px;
  height: 28px;
  background: #f4b3c2;
  color: #000;
  border-radius: 6px;
  font-weight: bold;
  font-size: 0.9rem;
  font-style: normal;
}

@keyframes slow-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .zen-container {
    padding: 0 1.5rem;
    gap: 4rem;
  }
  .block-intro {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
    border: none;
  }
  .zen-hero-name {
    border-right: none;
    padding-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 2rem;
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
  }
  .block-status {
    flex-direction: column;
    padding: 2rem;
    gap: 4rem;
    text-align: center;
  }
  .zen-avatar-system {
    width: 100%;
    height: 350px;
    transform: scale(0.8);
  }
  .z-capsule {
    position: relative;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    margin: 10px 0;
  }
  .zen-avatar-system {
    flex-direction: column;
    height: auto;
    gap: 1rem;
  }
  .enso-circle {
    display: none;
  }
  .floating-grid {
    grid-template-columns: 1fr;
  }
  .factory-split {
    flex-direction: column;
  }
  .f-left,
  .f-right {
    padding: 2rem;
  }
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
}

.h-card-front {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 2px;
  overflow: hidden;
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

.footer-section {
  padding: 20vh 10vw 10vh 10vw;
  background: #030305;
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
}
</style>
