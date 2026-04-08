<template>
  <div class="warm-os-container">
    <!-- 全局独立的 Tooltip 层，防止被溢出隐藏切割 -->
    <div
      class="global-tooltip"
      :class="{ show: activeTooltip }"
      :style="{ left: tooltipX + 'px', bottom: tooltipY + 'px' }"
    >
      {{ activeTooltip }}
    </div>

    <!-- 系统状态面板 -->
    <SystemPanel v-model="showPanel" />

    <div
      class="nav-trigger-area"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
    >
      <!-- 主控岛容器：管理高度、宽度过渡及溢出隐藏 -->
      <div class="island-wrapper" :class="viewState">
        <LiquidGlass
          :border-radius="viewState === 'pill' ? '24px' : '28px'"
          bg-color="rgba(255, 255, 255, 0.2)"
          class="island-glass"
        >
          <div class="island-content" @click.stop>
            <!-- 1. 收缩状态：状态栏 (Pill) -->
            <div class="island-status" :class="{ hide: viewState !== 'pill' }">
              <div class="status-left" @click.stop="toggleNavPanel">
                <i :class="['fa', currentIcon, 'status-icon']"></i>
                <span class="status-text">{{ currentMenuName }}</span>
              </div>
              <div class="status-right" @click.stop="toggleSystemPanel">
                {{ currentTime }}
              </div>
            </div>

            <!-- 2. 二次展开：开始菜单 (Menu) -->
            <div class="island-menu" :class="{ show: viewState === 'menu' }">
              <!-- 预留的顶部间距 -->
              <div class="menu-spacer"></div>
              <!-- 全局搜索框 -->
              <div class="search-box-wrapper">
                <div class="search-box">
                  <i class="fa fa-search search-icon"></i>
                  <input
                    type="text"
                    placeholder="探索博客内容..."
                    class="search-input"
                  />
                </div>
              </div>

              <div class="start-content">
                <div class="section-title">所有页面</div>
                <div class="nav-panel-grid">
                  <router-link
                    v-for="item in navItems"
                    :key="item.path"
                    :to="item.path"
                    class="nav-grid-item"
                    :class="{ active: route.path === item.path }"
                    @click="showNavPanel = false"
                  >
                    <div class="icon-wrapper">
                      <i :class="['fa fa-lg', item.icon]"></i>
                    </div>
                    <span>{{ item.name }}</span>
                  </router-link>
                </div>

                <div class="section-title mt-4">常用应用</div>
                <div class="nav-panel-list">
                  <div class="app-list-item" @click="showNavPanel = false">
                    <i class="fa fa-window-maximize text-blue-500"></i>
                    <span>Terminal</span>
                  </div>
                  <div class="app-list-item" @click="showNavPanel = false">
                    <i class="fa fa-folder-open text-yellow-500"></i>
                    <span>文件管理器</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 3. 展开状态：应用 Dock 栏 -->
            <div class="island-dock" :class="{ show: viewState !== 'pill' }">
              <!-- 主菜单徽标 -->
              <div
                class="dock-item"
                :class="{ active: showNavPanel }"
                @click.stop="toggleNavPanel"
                @mouseenter="showTooltip($event, '主菜单')"
                @mouseleave="hideTooltip"
              >
                <i class="fa fa-lg dock-icon fa-th-large"></i>
              </div>

              <div class="divider"></div>

              <!-- 应用图标区 -->
              <div
                class="dock-item"
                @mouseenter="showTooltip($event, '浏览器')"
                @mouseleave="hideTooltip"
              >
                <i
                  class="fa fa-lg dock-icon fa-chrome"
                  style="color: #4285f4"
                ></i>
              </div>

              <div
                class="dock-item"
                @mouseenter="showTooltip($event, '终端')"
                @mouseleave="hideTooltip"
              >
                <i
                  class="fa fa-lg dock-icon fa-terminal"
                  style="color: #333"
                ></i>
              </div>

              <div class="divider"></div>

              <!-- 实时 FPS 显示 -->
              <div class="dock-fps-widget" title="当前帧率">
                <span class="fps-value" :style="{ color: fps >= 45 ? '#10b981' : (fps >= 30 ? '#f59e0b' : '#ef4444') }">{{ fps }}</span>
                <span class="fps-label">FPS</span>
              </div>

              <div class="divider"></div>

              <!-- 系统时间和状态入口 -->
              <div class="dock-time-widget" @click.stop="toggleSystemPanel">
                <span class="time-main">{{ currentTimeSplit.time }}</span>
                <span class="time-sub">{{ currentTimeSplit.date }}</span>
              </div>
            </div>
          </div>
        </LiquidGlass>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import LiquidGlass from "../LiquidGlass.vue";
import SystemPanel from "./SystemPanel.vue";

const route = useRoute();

// UI 核心状态
const isHovered = ref(false);
const showNavPanel = ref(false); // 控制二次展开 (Start Menu)
const showPanel = ref(false); // 控制侧边系统状态栏

// 混合计算得到的视图状态：'pill' (收缩) | 'dock' (展开条) | 'menu' (二次展开面)
const viewState = computed(() => {
  if (showNavPanel.value) return "menu";
  if (isHovered.value) return "dock";
  return "pill";
});

// 全局 Tooltip 状态控制，解决 overflow:hidden 切割问题
const activeTooltip = ref("");
const tooltipX = ref(0);
const tooltipY = ref(0);

const showTooltip = (e: MouseEvent, text: string) => {
  activeTooltip.value = text;
  const target = e.currentTarget as HTMLElement;
  const rect = target.getBoundingClientRect();
  tooltipX.value = rect.left + rect.width / 2;
  // 加上一些上方间距，56 = icon 高度(44) + 悬浮距离(12)
  tooltipY.value = window.innerHeight - rect.top + 8;
};

const hideTooltip = () => {
  activeTooltip.value = "";
};

// 交互操作
const handleMouseEnter = () => {
  isHovered.value = true;
};

const handleMouseLeave = () => {
  // 鼠标离开触发区时，只有当**菜单未打开**时才回缩。
  // 这防止了鼠标划入变长菜单时发生“鬼畜”回落。
  isHovered.value = false;
  hideTooltip();
};

const toggleSystemPanel = () => {
  showPanel.value = !showPanel.value;
  if (showPanel.value) showNavPanel.value = false;
};

const toggleNavPanel = () => {
  showNavPanel.value = !showNavPanel.value;
  if (showNavPanel.value) showPanel.value = false;
};

const closePanels = () => {
  showPanel.value = false;
  showNavPanel.value = false;
};

// 导航数据
const navItems = ref([
  { name: "首页", path: "/home", icon: "fa-home" },
  { name: "文章", path: "/article", icon: "fa-file-text" },
  { name: "归档", path: "/archive", icon: "fa-archive" },
  { name: "随谈", path: "/diary", icon: "fa-comments" },
  { name: "友链", path: "/friend", icon: "fa-users" },
]);

const currentMenuName = computed(() => {
  const item =
    navItems.value.find(
      (i) => route.path.startsWith(i.path) && i.path !== "/",
    ) || navItems.value[0];
  if (route.path === "/" || route.path === "/home")
    return navItems.value[0]?.name ?? "首页";
  return item?.name || "应用容器";
});

const currentIcon = computed(() => {
  const item =
    navItems.value.find(
      (i) => route.path.startsWith(i.path) && i.path !== "/",
    ) || navItems.value[0];
  if (route.path === "/" || route.path === "/home")
    return navItems.value[0]?.icon ?? "fa-home";
  return item?.icon || "fa-compass";
});

// 时间管理
const currentTime = ref("");
const currentTimeSplit = ref({ time: "", date: "" });
let timer: ReturnType<typeof setInterval>;

const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  });
  currentTimeSplit.value = {
    time: now.toLocaleTimeString("zh-CN", {
      hour: "2-digit",
      minute: "2-digit",
    }),
    date: now.toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" }),
  };
};

// ================ FPS 监测 ================
const fps = ref(0);
let frameCount = 0;
let lastFrameTime = performance.now();
let fpsAnimationId: number;

const calculateFPS = () => {
  const now = performance.now();
  frameCount++;
  if (now - lastFrameTime >= 1000) {
    fps.value = Math.round((frameCount * 1000) / (now - lastFrameTime));
    frameCount = 0;
    lastFrameTime = now;
  }
  fpsAnimationId = requestAnimationFrame(calculateFPS);
};

onMounted(() => {
  updateTime();
  timer = setInterval(updateTime, 1000);
  fpsAnimationId = requestAnimationFrame(calculateFPS);
  document.addEventListener("click", closePanels);
});

onUnmounted(() => {
  clearInterval(timer);
  cancelAnimationFrame(fpsAnimationId);
  document.removeEventListener("click", closePanels);
});
</script>

<style scoped>
.warm-os-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 0;
  z-index: 100;
  pointer-events: none; /* 允许鼠标穿透到底层页面 */
}

/* Tooltip 不在溢出隐藏容器内，自由设定位置和淡入动画 */
.global-tooltip {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
  opacity: 0;
  transform: translateX(-50%) translateY(8px);
  transition:
    opacity 0.2s cubic-bezier(0.34, 1.56, 0.64, 1),
    transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 1000;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
@media (prefers-color-scheme: dark) {
  .global-tooltip {
    background-color: rgba(255, 255, 255, 0.85);
    color: #000;
  }
}
.global-tooltip.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* 页面底部的事件热区 */
.nav-trigger-area {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 600px;
  height: 100px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 24px; /* 离底部的距离 */
  pointer-events: auto; /* 恢复交互 */
}

/* ================= 核心结构重构 ================= */
.island-wrapper {
  position: relative;
  /* 平滑的尺寸控制，这三者是灵动岛动画顺滑的关键 */
  transition:
    max-width 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
    height 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
    transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  /* 基础弹性轴 */
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  /* 恢复 overflow: hidden！这是苹果式灵动岛裁剪内容毛边的关键。
     由于 Tooltip 已经完全独立全局，不再被裁剪，这里可以安全使用！ */
  overflow: hidden;
  /* 阴影悬浮感 */
  box-shadow:
    0 12px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 1px rgba(255, 255, 255, 0.6);
  border-radius: 24px;
}
@media (prefers-color-scheme: dark) {
  .island-wrapper {
    box-shadow:
      0 12px 32px rgba(0, 0, 0, 0.4),
      inset 0 1px 1px rgba(255, 255, 255, 0.1);
  }
}

/* 玻璃层贴合并占据所有体积 */
.island-glass {
  width: 100%;
  height: 100%;
  /* 移除 absolute 定位，让它作为常规内容存在，从而把内部尺寸透传给 wrapper */
  border-radius: inherit;
  transition: border-radius 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden; /* 恢复完美的背景圆角切除 */
}

/* == 状态尺码控制 == */
/* 1. Pill 收缩态 */
.island-wrapper.pill {
  max-width: 170px;
  height: 48px;
  transform: translateY(4px) scale(0.96);
  border-radius: 24px;
}

/* 2. Dock 展开态 */
.island-wrapper.dock {
  max-width: 800px;
  height: 60px;
  transform: translateY(0) scale(1);
  border-radius: 28px;
}

/* 3. Menu 二次展开高态 */
.island-wrapper.menu {
  max-width: 800px; /* 依据内部内容(也就是底框)撑开最大边界 */
  height: 480px; /* 二次平滑拔高！ */
  transform: translateY(0) scale(1);
  border-radius: 32px;
}

/* 控制内部元素，使得它在横向自适应宽度，从而撑开 wrapper 到 max-width 极限 */
.island-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: max-content; /* 最核心魔法：由内部内容驱动容器实际宽度！ */
  height: 100%; /* 满高，供 flex 自动布局 */
  margin: 0 auto;
}

/* ======== 第一层：状态栏 (Pill) ======== */
.island-status {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%; /* 撑满当前灵动岛宽度 */
  height: 48px; /* 固定为短条状态的高度 */
  box-sizing: border-box; /* 确保 padding 不会撑破容器 */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px;
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
  transition:
    opacity 0.25s ease 0.1s,
    transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 10;
}
.island-status.hide {
  opacity: 0;
  transform: scale(0.9);
  pointer-events: none;
  transition:
    opacity 0.15s ease,
    transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.status-left {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  margin-left: -8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  overflow: hidden;
  white-space: nowrap;
}
.status-left:hover {
  background-color: rgba(0, 0, 0, 0.05);
}
@media (prefers-color-scheme: dark) {
  .status-left:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
}

.status-icon {
  color: #555;
  font-size: 14px;
}
.status-text {
  font-size: 13px;
  font-weight: 500;
  color: #333;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.status-right {
  font-size: 12px;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  padding: 4px 8px;
  margin-right: -8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}
.status-right:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

@media (prefers-color-scheme: dark) {
  .status-icon {
    color: #ccc;
  }
  .status-text {
    color: #eee;
  }
  .status-right {
    color: #eee;
  }
  .status-right:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
}

/* ======== 第二层：主导航菜单 (Menu) ======== */
.island-menu {
  width: 360px;
  margin: 0 auto;
  opacity: 0;
  pointer-events: none;
  transform: translateY(20px) scale(0.95);
  transition:
    opacity 0.3s ease,
    transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  flex-direction: column;
  flex: 1; /* 撑满纵向高度，压住底部的 Dock */
  overflow: hidden; /* 防止未激活时内容干扰 */
}
.island-menu.show {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
}

.menu-spacer {
  height: 24px;
}

.search-box-wrapper {
  margin-bottom: 16px;
  padding: 0 16px;
}
.search-box {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  padding: 8px 16px;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.05) inset,
    0 1px 0 rgba(255, 255, 255, 0.5);
}
@media (prefers-color-scheme: dark) {
  .search-box {
    background: rgba(0, 0, 0, 0.3);
    box-shadow:
      0 2px 8px rgba(0, 0, 0, 0.3) inset,
      0 1px 0 rgba(255, 255, 255, 0.05);
  }
}
.search-icon {
  color: #666;
  margin-right: 8px;
}
.search-input {
  border: none;
  background: transparent;
  outline: none;
  flex: 1;
  font-size: 14px;
  color: #333;
}
.search-input::placeholder {
  color: #999;
}
@media (prefers-color-scheme: dark) {
  .search-icon {
    color: #aaa;
  }
  .search-input {
    color: #eee;
  }
  .search-input::placeholder {
    color: #666;
  }
}

.start-content {
  padding: 0 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-bottom: 12px;
  padding-left: 4px;
}
@media (prefers-color-scheme: dark) {
  .section-title {
    color: #aaa;
  }
}
.mt-4 {
  margin-top: 16px;
}

.nav-panel-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  row-gap: 20px;
  column-gap: 16px;
  justify-items: center;
}
.nav-grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #333;
  width: 100%;
  transition: transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.nav-grid-item:hover {
  transform: scale(1.05);
}
@media (prefers-color-scheme: dark) {
  .nav-grid-item {
    color: #eee;
  }
}

.nav-grid-item .icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 8px;
  color: #555;
  transition: background-color 0.2s;
}
.nav-grid-item:hover .icon-wrapper {
  background-color: rgba(255, 255, 255, 0.9);
}
.nav-grid-item.active .icon-wrapper {
  background-color: #0078d4;
  color: white;
}
@media (prefers-color-scheme: dark) {
  .nav-grid-item .icon-wrapper {
    background-color: rgba(255, 255, 255, 0.1);
    color: #ddd;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }
  .nav-grid-item:hover .icon-wrapper {
    background-color: rgba(255, 255, 255, 0.2);
  }
  .nav-grid-item.active .icon-wrapper {
    background-color: #005a9e;
  }
}
.nav-grid-item span {
  font-size: 12px;
  font-weight: 500;
}

.nav-panel-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.app-list-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s;
}
.app-list-item i {
  margin-right: 12px;
  width: 20px;
  text-align: center;
}
.app-list-item span {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}
.app-list-item:hover {
  background: rgba(255, 255, 255, 0.8);
}
@media (prefers-color-scheme: dark) {
  .app-list-item {
    background: rgba(255, 255, 255, 0.05);
  }
  .app-list-item span {
    color: #eee;
  }
  .app-list-item:hover {
    background: rgba(255, 255, 255, 0.15);
  }
}

/* ======== 第三层：应用底座 (Dock) ======== */
.island-dock {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  /* 初始不可见并略微缩小，等待 wrapper 拓宽 */
  opacity: 0;
  transform: translateY(10px) scale(0.9);
  pointer-events: none;
  transition:
    opacity 0.3s ease,
    transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 10;
  height: 60px; /* 固定高宽，为整个组件奠定拓宽基础 */
  flex-shrink: 0;
}
.island-dock.show {
  /* 当激活 dock/menu 时，内部模块迅速淡入 */
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
  /* 为了能让淡入和 wrapper 扩宽协调，加一点延迟 */
  transition:
    opacity 0.35s ease 0.15s,
    transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s;
}

.dock-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}
.dock-icon {
  color: #444;
  transition: color 0.3s ease;
}
@media (prefers-color-scheme: dark) {
  .dock-icon {
    color: #ddd;
  }
}

.dock-item:hover {
  background-color: rgba(255, 255, 255, 0.6);
  transform: translateY(-6px);
}
.dock-item.active {
  background-color: rgba(255, 255, 255, 0.8);
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
@media (prefers-color-scheme: dark) {
  .dock-item:hover {
    background-color: rgba(255, 255, 255, 0.15);
  }
  .dock-item.active {
    background-color: rgba(255, 255, 255, 0.25);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }
}

.divider {
  width: 1px;
  height: 28px;
  background-color: rgba(0, 0, 0, 0.15);
  margin: 0 2px;
  border-radius: 1px;
}
@media (prefers-color-scheme: dark) {
  .divider {
    background-color: rgba(255, 255, 255, 0.2);
  }
}

.dock-time-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 10px;
  height: 44px;
  border-radius: 12px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  flex-shrink: 0;
}
.dock-time-widget:hover {
  background-color: rgba(0, 0, 0, 0.05);
}
.time-main {
  font-size: 13px;
  font-weight: 700;
  color: #333;
}
.time-sub {
  font-size: 10px;
  color: #666;
  margin-top: -2px;
}

/* ================ 实时 FPS 挂件 ================ */
.dock-fps-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 8px;
  height: 44px;
  flex-shrink: 0;
  cursor: default;
  user-select: none;
}
.fps-value {
  font-size: 13px;
  font-weight: 700;
}
.fps-label {
  font-size: 10px;
  color: #666;
  margin-top: -2px;
  font-weight: 600;
}

@media (prefers-color-scheme: dark) {
  .dock-time-widget:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  .time-main {
    color: #eee;
  }
  .time-sub {
    color: #aaa;
  }
  .fps-label {
    color: #aaa;
  }
}
</style>
