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
          晨煦的小窝 · <span class="highlight-gold">诗与暖阳</span>
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
                  烟花三月雨，滴碎万竿梢。翠影参差云外摇，清籁穿林杪。
                </div>
                <div class="zen-quote">
                  “发呆不是浪费生命，是给生命留出编译的时间。”
                </div>
              </div>
              <div class="status-text">
                <h3>我是一位“全干工程师”。</h3>
                <p>
                  写代码、聊哲学、推物理、焊电路、发呆、胡思乱想、吃白饭。总之啥都干。
                </p>
                <p class="status-summary">
                  🌸🌸🌸<br />
                  总幻想自己已不小心创造了AGI，<br />
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
                :size="260"
                class="zen-avatar-core"
              />
              <!-- 横版胶囊状态小组件 -->
              <div class="z-capsule cap-1">
                <span class="c-emoji">🍚</span>
                <div class="c-details">
                  <strong>吃白饭</strong><span>谁都阻止不了我干饭的热情</span>
                </div>
              </div>
              <div class="z-capsule cap-2">
                <span class="c-emoji">⌨️</span>
                <div class="c-details">
                  <strong>写代码</strong
                  ><span>Rust底层 / Py脚本 / TS类型体操</span>
                </div>
              </div>
              <div class="z-capsule cap-3">
                <span class="c-emoji">🪐</span>
                <div class="c-details">
                  <strong>聊哲学</strong><span>上帝已死！类型永存！</span>
                </div>
              </div>
              <div class="z-capsule cap-4">
                <span class="c-emoji">📐</span>
                <div class="c-details">
                  <strong>玩物理</strong><span>波粒二象性，启动！！！</span>
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

        <div class="float-windows-grid">
          <div class="float-window win-glass">
            <div class="win-dot red"></div>
            <div class="win-dot yellow"></div>
            <div class="win-dot green"></div>
            <h4>[ YaoXiang ]</h4>
            <p>
              该语言的豪言壮语：<strong>Type the Universe</strong>。<br />
              欢迎来点 star，或者点 issue 骂我。总之轻点喷。<br />
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
              深入学习计算机组成原理，希望有一天能为“多核原生”做出自己的贡献。毕竟现在谁没个十二核二十四线程的，总要有办法既简单又高效的利用多核吧？
            </p>
          </div>

          <div class="float-window win-agape">
            <div class="win-icon">⚙️</div>
            <h4>AGI 执念</h4>
            <p>
              听起来很中二，但我依旧是有着改变世界的余念：<br />实现能改变世界的
              AGI。
            </p>
          </div>

          <div class="float-window win-neuro">
            <div class="win-header">
              <strong>脑电 + MR + 3D眼动追踪</strong>
              <span class="win-badge">进度: 脑内地图中</span>
            </div>
            <p>
              这又是一个我想改变世界的方向。<br />
              <strong>具体来说</strong
              >：将手机屏幕放到MR中，并用脑电+眼动追踪来控制屏幕上的光标和输入。实现真正的无肢体交互。<br />
              <strong>我的目标是</strong>：成为下一个乔布斯！
            </p>
          </div>
        </div>

        <p class="ambition-footer v-observe reveal-up delay-2">
          对类型系统、计组、AGI、脑机接口感兴趣？欢迎脑暴。<strong
            >总之我什么都能聊~。</strong
          >
        </p>

        <!-- 板块四：技能模块 + 联系方式 -->
        <div class="zen-block block-factory v-observe reveal-up delay-3">
          <div class="factory-split">
            <div class="f-left">
              <h4>我会做什么？</h4>
              <ul class="f-list">
                <li>
                  <strong>全栈工程师</strong>：热烈推崇前后端分离， FastAPI
                  拥护者， Vue 爱好者，反对 Java 腐烂的 SpringBoot 。
                </li>
                <li>
                  <strong>Rust Leaner</strong>： Rust 重写一切！
                  内存安全、性能、优雅的类型系统，还有那令人愉悦的编译器错误提示，都是我爱上Rust的理由。
                </li>
                <li>
                  <strong>Nonebot2 开发者</strong>：经常写一些无厘头的 Bot
                  插件，比如话多排行榜，水印大师，抑或是？色色保存器？
                </li>
                <li>
                  <strong>热爱探索边界</strong>：硬件还是软件？ 系统编程 or
                  脚本编程，总之我全都要！
                </li>
                <li>
                  <strong>物理</strong
                  >：对世界的本质抱有朴素的直觉，相信一切都有大一统的美学，量子力学只是我的借口，真正的物理是数学！
                </li>
                <li>
                  <strong>AGI</strong
                  >：如果我是小说主角，我一定是那个改变世界的人！
                </li>
                <li>
                  <strong>形而上学砖家</strong
                  >：物理学的尽头是数学，数学的尽头是哲学，哲学的尽头是形而上。
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
                  > 可接发呆咨询，价格面议<br />
                </div>
                <div class="c-links">
                  <a
                    href="https://github.com/ChenXu233"
                    target="_blank"
                    class="c-btn"
                    ><i class="icon">G</i> GitHub</a
                  >
                  <a
                    href="https://www.xiaohongshu.com/user/profile/66b02a79000000001d0306be"
                    class="c-btn"
                    ><i class="icon">R</i> 小红书·牛肉厨</a
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

    <!-- Footer -->
    <section class="footer-section">
      <div class="bottomtip v-observe fade-in-scroll">
        <span class="tip-text">到这里结束啦，点击下方悬浮窗探索更多</span>
      </div>
      <div class="footer-note reveal-up v-observe">
        <span class="copyright">© 2026 ChenXuBlog</span>
        <span class="separator">·</span>
        <a
          href="https://beian.miit.gov.cn/"
          target="_blank"
          rel="noopener"
          class="icp-link"
          >浙ICP备2026024319号-1</a
        >
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import BlossomCanvas from "../components/effects/BlossomCanvas.vue";
import RainCanvas from "../components/effects/RainCanvas.vue";
import SunriseParallax from "../components/effects/SunriseParallax.vue";
import BambooParallax from "../components/effects/BambooParallax.vue";
const introSection = ref<HTMLElement | null>(null);

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

onMounted(() => {
  setupObserver();
  document.body.classList.add("home-hide-scrollbar");

  // Initial rain opacity is 0 if at top of page
  const mainRain = document.getElementById("rain-canvas");
  if (mainRain && window.scrollY < window.innerHeight * 0.2) {
    mainRain.style.opacity = "0";
  }

  window.addEventListener("scroll", handleTitleParallax, { passive: true });

  setTimeout(() => {
    document.querySelector(".hero-content")?.classList.add("is-revealed");
  }, 100);
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleTitleParallax);
  if (observer) observer.disconnect();
  document.body.classList.remove("home-hide-scrollbar");
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
  color: #f4b3c2;
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
  }
  .fused-left {
    flex: none;
    width: 100%;
    flex-direction: column;
    clip-path: none;
    padding: 3rem 1rem;
    text-align: center;
    align-items: center;
  }
  .zen-hero-name {
    padding-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 0rem;
    justify-content: center;
    gap: 1rem;
    font-size: 5rem;
    flex-direction: row;
  }
  .fused-right {
    flex: none;
    width: 100%;
    clip-path: none;
    padding: 1rem;
  }
  .zen-avatar-system {
    width: 100%;
    height: 350px;
    transform: scale(0.8);
  }
  .enso-circle {
    display: none;
  }
  .float-windows-grid {
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

/* Footer */
.footer-section {
  padding: 5vh 5vw 10vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.bottomtip {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 2rem;
  font-family: "PingFang SC", "Noto Sans SC", sans-serif;
  letter-spacing: 0.3em;
}

.tip-text {
  position: relative;
}

.tip-text::before,
.tip-text::after {
  content: "~";
  margin: 0 0.5em;
  opacity: 0.4;
}

.footer-note {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.8rem;
  letter-spacing: 1px;
}

.copyright {
  font-family: "JetBrains Mono", monospace;
}

.separator {
  opacity: 0.3;
}

.icp-link {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  font-family: "JetBrains Mono", monospace;
  transition: color 0.3s ease;
}

.icp-link:hover {
  color: #f4b3c2;
}

/* Responsive */
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

  .zen-container {
    padding: 0 1rem;
    gap: 3rem;
  }

  .zen-hero-name {
    font-size: 4rem;
    flex-direction: row;
    gap: 0.5rem;
    padding-bottom: 0rem;
  }

  .zen-prose {
    font-size: 1.1rem;
  }
  .zen-quote {
    font-size: 1.1rem;
  }

  .f-left,
  .f-right {
    padding: 1.5rem;
    flex: 1;
  }
  .float-window {
    padding: 1.5rem;
  }
}
</style>
