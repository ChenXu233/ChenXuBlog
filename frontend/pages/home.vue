<template>
  <div class="elegant-home">
    <div
      class="bg-transition-layer"
      :style="{ opacity: Math.min(1, scrollProgress * 1.5) }"
    ></div>

    <BlossomCanvas />
    <RainCanvas />

    <section class="hero-section">
      <SunriseParallax :progress="scrollProgress" />
      <div class="hero-content" ref="heroText">
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

    <section class="intro-section zen-canvas" ref="introSection">
      <BambooParallax :progress="bambooProgress" />
      <div class="zen-watermark">C.X_UNIVERSE</div>
      <div class="zen-container">
        <div class="zen-block block-fused">
          <div class="fused-left">
            <div class="zen-hero-name"><span>晨</span><span>煦</span></div>
            <div class="zen-text-col">
              <div class="zen-biography">
                <div class="zen-subtitle">ChenXu233 // SYS.ADMIN</div>
                <div class="zen-prose">
                  烟花三月雨，滴碎万竿梢。翠影参差云外摇，清籁穿林杪。
                </div>
                <div class="zen-quote">
                  "发呆不是浪费生命，是给生命留出编译的时间。"
                </div>
              </div>
              <div class="status-text">
                <h3>我是一位"全干工程师"。</h3>
                <p>
                  写代码、聊哲学、推物理、焊电路、发呆、胡思乱想、吃白饭。总之啥都干。
                </p>
              </div>
            </div>
          </div>
          <div class="fused-right">
            <div class="zen-avatar-system">
              <div class="enso-circle"></div>
              <img
                src="https://avatars.githubusercontent.com/u/91937041?v=4"
                class="w-48 h-48 rounded-full object-cover"
              />
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
              该语言的豪言壮语：<strong>Type the Universe</strong>。<br /><a
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
              深入学习计算机组成原理，希望有一天能为"多核原生"做出自己的贡献。
            </p>
          </div>
          <div class="float-window win-agape">
            <div class="win-icon">⚙️</div>
            <h4>AGI 执念</h4>
            <p>实现能改变世界的 AGI。</p>
          </div>
          <div class="float-window win-neuro">
            <div class="win-header">
              <strong>脑电 + MR + 3D眼动追踪</strong
              ><span class="win-badge">进度: 脑内地图中</span>
            </div>
            <p>
              将手机屏幕放到MR中，并用脑电+眼动追踪来控制屏幕上的光标和输入。
            </p>
          </div>
        </div>

        <div class="zen-block block-factory">
          <div class="factory-split">
            <div class="f-left">
              <h4>我会做什么？</h4>
              <ul class="f-list">
                <li><strong>全栈工程师</strong>：FastAPI + Vue 爱好者</li>
                <li><strong>Rust Learner</strong>：Rust 重写一切！</li>
                <li>
                  <strong>Nonebot2 开发者</strong>：经常写一些无厘头的 Bot 插件
                </li>
                <li><strong>热爱探索边界</strong>：硬件还是软件？我全都要！</li>
              </ul>
            </div>
            <div class="f-right">
              <div class="contact-box">
                <div class="c-greeting">
                  如果你也喜欢在代码里藏一点浪漫——很高兴认识你。
                </div>
                <div class="c-links">
                  <a
                    href="https://github.com/ChenXu233"
                    target="_blank"
                    class="c-btn"
                    >GitHub</a
                  >
                  <a href="mailto:chenxu233@type.universe" class="c-btn"
                    >chenxu233@type.universe</a
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="footer-section">
      <div class="footer-note">
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
useSeo();

const scrollProgress = ref(0);
const bambooProgress = ref(0);
const introSection = ref<HTMLElement | null>(null);

const handleScroll = () => {
  const scrollY = window.scrollY;
  const wh = window.innerHeight;
  const progress = Math.min(scrollY / wh, 1);
  scrollProgress.value = progress;

  if (introSection.value) {
    const rect = introSection.value.getBoundingClientRect();
    const distanceScrolled = wh - rect.top;
    bambooProgress.value = Math.max(0, Math.min(1, distanceScrolled / wh));
  }
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll, { passive: true });
  setTimeout(() => {
    document.querySelector(".hero-content")?.classList.add("is-revealed");
  }, 100);
});
onUnmounted(() => window.removeEventListener("scroll", handleScroll));
</script>

<style scoped>
.elegant-home {
  color: #fff;
  font-family: "JetBrains Mono", monospace;
  overflow-x: clip;
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
  background: #6a7664;
  z-index: -1;
  pointer-events: none;
}
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
  margin-top: -10vh;
}
.elegant-title {
  font-family: "Inter", "PingFang SC", sans-serif;
  line-height: 1.4;
  margin: 0;
  font-weight: 300;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}
.title-line {
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
  font-weight: 800;
  opacity: 0.8;
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
  gap: 6px;
  opacity: 0.6;
}
.line-indicator {
  width: 30px;
  height: 2px;
  background-color: #d4c5b0;
}
.zen-canvas {
  position: relative;
  width: 100vw;
  min-height: 100vh;
  padding: 8rem 0;
  display: flex;
  justify-content: center;
  font-family: "PingFang SC", "Noto Sans SC", sans-serif;
  color: #3a3a3a;
}
.zen-watermark {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 15vw;
  font-weight: 900;
  color: rgba(90, 90, 90, 0.03);
  pointer-events: none;
  z-index: 0;
  white-space: nowrap;
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
.block-fused {
  display: flex;
  align-items: stretch;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 500px;
}
.fused-left {
  flex: 0 0 60%;
  display: flex;
  flex-direction: row;
  padding: 3rem;
  gap: 2rem;
}
.fused-right {
  flex: 0 0 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem;
}
.zen-hero-name {
  display: flex;
  flex-direction: column;
  font-size: 5rem;
  font-weight: 500;
  letter-spacing: 0.3rem;
  color: #fff;
  padding-right: 2rem;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}
.zen-text-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
}
.zen-subtitle {
  font-family: "JetBrains Mono", monospace;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9rem;
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
}
.status-text h3 {
  font-size: 2rem;
  font-weight: 600;
  color: #f4b3c2;
}
.status-text p {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}
.enso-circle {
  position: absolute;
  width: 250px;
  height: 250px;
  border-radius: 50%;
  border: 1px dashed rgba(255, 255, 255, 0.1);
}
.float-windows-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}
.float-window {
  background: rgba(25, 28, 36, 0.4);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 2.5rem;
  transition: all 0.3s;
}
.float-window:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
}
.float-window h4 {
  font-size: 1.4rem;
  color: #f4b3c2;
  margin-bottom: 1.2rem;
}
.float-window p {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.65);
  line-height: 1.8;
}
.win-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 6px;
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
}
.win-agape {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.win-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
.win-badge {
  background: rgba(244, 179, 194, 0.15);
  color: #f4b3c2;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
}
.factory-split {
  display: flex;
  background: rgba(17, 19, 26, 0.6);
  border-radius: 24px;
  overflow: hidden;
}
.f-left {
  flex: 55%;
  padding: 4rem;
}
.f-left h4 {
  font-size: 1.6rem;
  color: #e2e8f0;
  margin-bottom: 2rem;
}
.f-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.f-list li {
  color: rgba(255, 255, 255, 0.6);
  padding-left: 2rem;
  position: relative;
}
.f-list li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #f4b3c2;
}
.f-right {
  flex: 45%;
  padding: 4rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.c-greeting {
  font-size: 1.1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
}
.c-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.c-btn {
  display: flex;
  align-items: center;
  padding: 1.2rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  color: #e2e8f0;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s;
}
.c-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateX(5px);
}
.footer-section {
  padding: 5vh 5vw 10vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.footer-note {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.8rem;
}
.copyright {
  font-family: "JetBrains Mono", monospace;
}
.icp-link {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
}
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
  .block-fused {
    flex-direction: column;
  }
  .fused-left,
  .fused-right {
    flex: none;
    width: 100%;
  }
  .float-windows-grid {
    grid-template-columns: 1fr;
  }
  .factory-split {
    flex-direction: column;
  }
}
</style>
