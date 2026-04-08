<template>
  <div class="elegant-home">
    <!-- Background Transition Layer (White to Bamboo Green) -->
    <div
      class="bg-transition-layer"
      :style="{ opacity: Math.min(1, scrollProgress * 1.2) }"
    ></div>

    <!-- Global Effects -->
    <BlossomCanvas />
    <RainCanvas />

    <!-- Section 1: Hero (Blossoms) -->
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

    <!-- Section 2: Progressive Introduction with Rain & Thunder -->
    <section class="intro-section zen-canvas" ref="introSection">
      <!-- 视差生长的竹子背景 -->
      <BambooParallax :progress="bambooProgress" />

      <div class="zen-watermark v-observe fade-in-scroll">C.X_UNIVERSE</div>

      <div class="zen-container">
        <!-- 融合板块：梯形布局（1/3文字 + 2/3头像系统） -->
        <div class="zen-block block-fused v-observe reveal-up">
          <!-- 左侧梯形 - 文字区域 -->
          <div class="fused-left">
            <div class="zen-hero-name">
              <span>晨</span>
              <span>煦</span>
            </div>
            <div class="zen-text-col">
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
              <div class="status-text">
                <h3>我是一位”全干工程师”。</h3>
                <p>
                  写代码、聊哲学、推物理、焊电路、发呆、胡思乱想、吃白饭。总之啥都干。
                </p>
                <p class="status-summary">
                  🌸🌸🌸<br />
                  幻想自己已不小心创造了AGI，<br />
                  思考宇宙的本源却发现世界就是一个巨大的自指悖论。<br />
                  把思绪写成诗，把春光当作背景，欢迎来到我的思维宇宙~ <br />
                  🌸🌸🌸
                </p>
              </div>
            </div>
          </div>

          <!-- 右侧梯形 - Avatar系统 -->
          <div class="fused-right">
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
        </div>

        <!-- 板块三：技术野心 (Floating Windows 巧思) -->
        <div class="ambition-header v-observe reveal-up delay-2">
          探 索 边 界 // EXPLORATION
        </div>

        <div class="float-windows-grid">
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
              深入学习计算机组成原理，希望有一天能为”多核原生”做出自己的贡献，让软件和硬件不再互相甩锅。
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
              目前能分辨”我在发呆”和”认真想bug”的区别。
            </p>
          </div>
        </div>

        <p class="ambition-footer v-observe reveal-up delay-2">
          对类型系统、计组、AGI、脑机接口感兴趣？欢迎脑暴。<strong
            >发呆小广告位常年招租。</strong
          >
        </p>

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
        <!-- 视差背景图层 -->
        <div class="h-parallax-bgs" ref="hParallaxBgs">
          <div v-for="(n, i) in 4" :key="n" class="h-bg-wrapper">
            <div
              class="h-bg-image"
              :ref="
                (el) => {
                  if (el) listBgImages[i] = el as HTMLElement;
                }
              "
              :style="{
                backgroundImage: `url(https://picsum.photos/seed/${
                  n * 35
                }/1920/1080)`,
              }"
            ></div>
          </div>
        </div>

        <div class="h-scroll-track" ref="hScrollTrack">
          <!-- Card 1 -->
          <div class="h-scroll-panel">
            <LiquidGlass>
              <div class="h-card-content">
                <span class="h-index">01</span>
                <h2>ARTICLES <span class="cn-text">文章</span></h2>
                <p>记录代码与灵感的灵光一现。</p>
                <router-link to="/article" class="explore-btn"
                  >Enter Module_</router-link
                >
              </div>
            </LiquidGlass>
          </div>
          <!-- Card 2 -->
          <div class="h-scroll-panel">
            <LiquidGlass>
              <div class="h-card-content">
                <span class="h-index">02</span>
                <h2>ARCHIVE <span class="cn-text">归档</span></h2>
                <p>时间轴上铭刻的所有过往与踪迹。</p>
                <router-link to="/archive" class="explore-btn"
                  >Enter Module_</router-link
                >
              </div>
            </LiquidGlass>
          </div>
          <!-- Card 3 -->
          <div class="h-scroll-panel">
            <LiquidGlass>
              <div class="h-card-content">
                <span class="h-index">03</span>
                <h2>LINKS <span class="cn-text">友链</span></h2>
                <p>数字航海家的中转站与星图网路。</p>
                <router-link to="/friend" class="explore-btn"
                  >Enter Module_</router-link
                >
              </div>
            </LiquidGlass>
          </div>
          <!-- Card 4 -->
          <div class="h-scroll-panel">
            <LiquidGlass>
              <div class="h-card-content">
                <span class="h-index">04</span>
                <h2>DIARY <span class="cn-text">随谈</span></h2>
                <p>抛开代码架构，回归纯粹的片语轻言。</p>
                <router-link to="/diary" class="explore-btn"
                  >Enter Module_</router-link
                >
              </div>
            </LiquidGlass>
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
import CyberMonitor from "../components/CyberMonitor.vue";
import SunriseParallax from "../components/effects/SunriseParallax.vue";
import BambooParallax from "../components/effects/BambooParallax.vue";
const introSection = ref<HTMLElement | null>(null);
const introSectionHeight = ref<number | undefined>(undefined);

const hScrollWrapper = ref<HTMLElement | null>(null);
const hScrollTrack = ref<HTMLElement | null>(null);
const hParallaxBgs = ref<HTMLElement | null>(null);
const listBgImages = ref<HTMLElement[]>([]);

const scrollProgress = ref(0);
const bambooProgress = ref(0);

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

// Global Scroll Progression & Effects
const handleTitleParallax = () => {
  const scrollY = window.scrollY;
  const wh = window.innerHeight;
  const progress = Math.min(scrollY / wh, 1);
  scrollProgress.value = progress;

  // 竹子视差计算 (intro-section 滚动进度)
  // 当 introSection 的 top 从 wh 减小到 0 时，bambooProgress 从 0 增长到 1
  if (introSection.value) {
    const rect = introSection.value.getBoundingClientRect();
    const distanceScrolled = wh - rect.top;
    bambooProgress.value = Math.max(0, Math.min(1, distanceScrolled / wh));
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

  // 同步视差背景容器的位置
  if (hParallaxBgs.value) {
    hParallaxBgs.value.style.transform = `translate3d(-${
      progress * 75
    }%, 0, 0)`;
  }

  // 计算每个视差背景的相对位置和接管阈值
  listBgImages.value.forEach((img, i) => {
    // localOffset 范围：-i 到 3-i。当局部进度为 0 时，说明这块卡片在正中间
    const localOffset = progress * 3 - i;
    const isTakeover = Math.abs(localOffset) < 0.15; // 居中阈值

    if (isTakeover) {
      img.classList.add("is-takeover");
      img.style.transform = `translate3d(0, 0, 0) scale(1)`; // 直接弹入，缩放到1
    } else {
      img.classList.remove("is-takeover");
      // 视差位移：每远离 1 个卡面宽度，对应背景位移部分 20%
      img.style.transform = `translate3d(${
        localOffset * 20
      }%, 0, 0) scale(1.1)`;
    }
  });
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
  background: transparent;
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
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
  /* right-align or adjust if needed */
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

/* Section 2: Soft Zen Canvas */
.zen-canvas {
  position: relative;
  width: 100vw;
  min-height: 100vh;
  margin-left: calc(-50vw + 50%);
  padding: 8rem 0;
  display: flex;
  justify-content: center;
  background: transparent;
  font-family: "PingFang SC", "Noto Sans SC", sans-serif;
  color: #3a3a3a; /* Adjusted to dark for light background */
  overflow: visible; /* 允许竹子向上溢出抵达 Section 1 */
}

.zen-watermark {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 15vw;
  font-family: "JetBrains Mono", monospace;
  font-weight: 900;
  color: rgba(90, 90, 90, 0.03); /* subtle dark watermark */
  letter-spacing: -2px;
  pointer-events: none;
  z-index: 0;
  white-space: nowrap;
}

.zen-block {
  z-index: 2;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
}

.zen-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1400px;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 8rem;
}

/* BLOCK FUSED: 梯形融合布局（1/3文字 + 2/3头像） */
.block-fused {
  display: flex;
  align-items: stretch;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  overflow: visible;
  min-height: 500px;
  isolation: isolate;
}

/* 左侧梯形 - 文字区域 */
.fused-left {
  flex: 0 0 60%;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  padding: 3rem;
  gap: 2rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), transparent);
  position: relative;
  z-index: 2;
}

/* 右侧梯形 - Avatar区域 */
.fused-right {
  flex: 0 0 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem;
  position: relative;
  z-index: 1;
}

/* 晨煦名字 - 水平排列，最左边 */
.zen-hero-name {
  display: flex;
  position: relative;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 5rem;
  font-weight: 500;
  letter-spacing: 0.3rem;
  color: #fff;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
  padding-right: 2rem;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

/* 文字内容列 - biography + status */
.zen-text-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
}
.zen-biography {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.zen-subtitle {
  font-family: "JetBrains Mono", monospace;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9rem;
  letter-spacing: 2px;
}
.zen-prose {
  font-size: 1.5rem;
  font-weight: bold;
  line-height: 1.6;
}
.hl-soft {
  color: #f4b3c2;
  font-family: "JetBrains Mono";
  font-weight: bold;
}
.zen-quote {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.6);
  border-left: 2px solid rgba(255, 255, 255, 0.2);
  padding-left: 1rem;
  font-style: italic;
}
.status-text {
  max-width: none;
}
.status-text h3 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #f4b3c2;
}
.status-text p {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 1rem;
}
.status-summary {
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem 1.2rem;
  border-radius: 12px;
  border-left: 3px solid rgba(244, 179, 194, 0.4);
  font-size: 0.9rem !important;
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
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
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
.ambition-header {
  font-size: 1rem;
  letter-spacing: 4px;
  color: rgba(255, 255, 255, 0.3);
  text-align: center;
  font-family: "JetBrains Mono", monospace;
  margin-bottom: -4rem;
}
.float-windows-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-bottom: -5rem;
}
.float-window {
  position: relative;
  background: rgba(25, 28, 36, 0.4);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 2.5rem;
  transition: all 0.3s ease;
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
  margin-top: 2rem;
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
  .block-fused {
    flex-direction: column;
    min-height: auto;
    gap: 3rem;
  }
  .fused-left {
    flex: none;
    width: 100%;
    clip-path: none;
    padding: 3rem 2rem;
    text-align: center;
    align-items: center;
  }
  .zen-hero-name {
    border-right: none;
    padding-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 1.5rem;
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
    font-size: 2.5rem;
  }
  .fused-right {
    flex: none;
    width: 100%;
    clip-path: none;
    padding: 2rem;
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
  background: #2a3136; /* 调整底色更深，映衬图片 */
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

.h-parallax-bgs {
  position: absolute;
  top: 0;
  left: 0;
  width: 400vw;
  height: 100vh;
  display: flex;
  z-index: -1;
  will-change: transform;
}

.h-bg-wrapper {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.h-bg-image {
  position: absolute;
  top: 0;
  left: -25vw;
  width: 150vw; /* 留出25vw的视差余裕 */
  height: 100%;
  background-size: cover;
  background-position: center;
  opacity: 0.15;
  filter: blur(4px) grayscale(50%);
  transform: translate3d(0, 0, 0) scale(1.1);
  transition:
    transform 0.6s cubic-bezier(0.25, 1, 0.5, 1),
    opacity 0.5s ease,
    filter 0.5s ease;
  will-change: transform, opacity, filter;
}

.h-bg-image.is-takeover {
  opacity: 0.6;
  filter: blur(0px) grayscale(0%);
  /* transform 被 JS 控制为弹入并居中 */
}

.h-scroll-track {
  display: flex;
  width: 400vw;
  height: 100%;
  will-change: transform;
  z-index: 1; /* 确保卡片在栏珊背景上方 */
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

.h-card-content {
  position: relative;
  z-index: 2;
  padding: 4rem;
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0) 100%
  );
  height: 50vh;
  width: 50vw;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.h-index {
  font-family: "Cinzel", serif;
  font-size: 5rem;
  color: rgba(255, 255, 255, 0.15);
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
  color: #fff;
}

.cn-text {
  font-family: "JetBrains Mono", monospace;
  font-size: 1.5rem;
  color: #ff7aa2;
}

.h-card-content p {
  font-size: 1.2rem;
  color: #ddd;
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
}
</style>
