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

    <!-- 动态全局右键菜单 -->
    <ContextMenu
      :visible="contextMenuVisible"
      :x="contextMenuX"
      :y="contextMenuY"
      :items="contextMenuItems"
      @update:visible="(val) => (contextMenuVisible = val)"
    />

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
          :border-radius="
            viewState === 'pill'
              ? 'calc(24 * var(--dk-u))'
              : 'calc(28 * var(--dk-u))'
          "
          :scale="dockUnit"
          bg-color="var(--dk-glass)"
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
                    v-model="searchKeyword"
                    placeholder="探索博客内容..."
                    class="search-input"
                    @keyup.enter="handleSearch"
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

                <div class="section-title mt-4">外观</div>
                <div class="theme-segment" role="group" aria-label="颜色模式">
                  <button
                    v-for="opt in themeOptions"
                    :key="opt.value"
                    type="button"
                    class="theme-option"
                    :class="{
                      active: mounted && colorMode.preference === opt.value,
                    }"
                    :aria-pressed="
                      mounted && colorMode.preference === opt.value
                    "
                    @click.stop="setThemePreference(opt.value)"
                  >
                    <i :class="['fa', opt.icon]"></i>
                    <span>{{ opt.label }}</span>
                  </button>
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

              <!-- 运行中的应用列表 -->
              <div
                v-for="app in openApps"
                :key="app.id"
                class="dock-item"
                :class="{
                  active: activeAppId === app.id,
                  minimized: app.minimized,
                }"
                @click.stop="toggleAppVisibility(app)"
                @contextmenu.prevent.stop="handleContextMenu($event, app)"
                @mouseenter="showTooltip($event, app.title)"
                @mouseleave="hideTooltip"
              >
                <i :class="['fa fa-lg dock-icon', app.icon]"></i>
                <div class="dock-indicator" v-if="activeAppId === app.id"></div>
              </div>

              <div class="divider"></div>

              <!-- 主题切换 -->
              <div
                class="dock-item dock-theme"
                role="button"
                tabindex="0"
                title="切换主题"
                @click.stop="toggleTheme"
                @keydown.enter.prevent="toggleTheme"
                @mouseenter="showTooltip($event, '切换主题')"
                @mouseleave="hideTooltip"
              >
                <i
                  class="fa fa-lg fa-moon-o dock-icon dock-theme-icon dock-theme-moon"
                ></i>
                <i
                  class="fa fa-lg fa-sun-o dock-icon dock-theme-icon dock-theme-sun"
                ></i>
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
import { useRoute, useRouter } from "vue-router";
import LiquidGlass from "../common/LiquidGlass.vue";
import SystemPanel from "./SystemPanel.vue";
import ContextMenu, { type MenuItem } from "./ContextMenu.vue";
import {
  openApps,
  activeAppId,
  toggleAppVisibility,
  closeApp,
  minimizeApp,
  type AppConfig,
} from "@/stores/warmos";

const route = useRoute();
const router = useRouter();

// 全局搜索
const searchKeyword = ref("");
const handleSearch = () => {
  const kw = searchKeyword.value.trim();
  if (!kw) return;
  showNavPanel.value = false;
  isHovered.value = false;
  router.push({ path: "/article", query: { search: kw } });
};

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
  // 间距跟着 dock 的缩放单位走（与 CSS 里的 --dk-u 同一公式）
  tooltipY.value = window.innerHeight - rect.top + 8 * computeDockUnit();
};

const hideTooltip = () => {
  activeTooltip.value = "";
};

// 右键菜单状态
const contextMenuVisible = ref(false);
const contextMenuX = ref(0);
const contextMenuY = ref(0);
const contextMenuItems = ref<MenuItem[]>([]);

const handleContextMenu = (e: MouseEvent, app: AppConfig) => {
  contextMenuItems.value = [
    {
      label: app.minimized ? "恢复应用" : "最小化",
      icon: "fa-window-minimize",
      action: () => toggleAppVisibility(app),
    },
    { separator: true },
    {
      label: "退出应用",
      icon: "fa-times",
      color: "#ff5f56",
      action: () => closeApp(app.id),
    },
  ];

  contextMenuX.value = e.clientX;
  contextMenuY.value = e.clientY - 10;
  contextMenuVisible.value = true;
  hideTooltip();
};

const hideContextMenu = () => {
  contextMenuVisible.value = false;
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
  hideContextMenu();
};

// 导航数据
const navItems = ref([
  { name: "首页", path: "/home", icon: "fa-home" },
  { name: "WarmOS", path: "/warmos", icon: "fa-compass" },
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

// ================ 原生暗色切换 ================
const colorMode = useColorMode();
const isDark = computed(() => colorMode.value === "dark");
const mounted = ref(false);

// 与 CSS 的 --dk-u 同一公式：1440 宽 = 1，4K ≈ 1.75。
// 传给液态玻璃，让折射环厚度 / 内框圆角 / 位移量一起等比放大。
const dockUnit = ref(1);
const computeDockUnit = () =>
  Math.min(
    3,
    Math.max(1, Math.min(window.innerWidth / 1440, window.innerHeight / 900)),
  );
const updateDockUnit = () => {
  dockUnit.value = computeDockUnit();
};

const themeOptions = [
  { value: "light", label: "浅色", icon: "fa-sun-o" },
  { value: "dark", label: "深色", icon: "fa-moon-o" },
  { value: "system", label: "跟随系统", icon: "fa-desktop" },
] as const;

// 选中态只在客户端渲染，避免 SSR 与 color-mode 注入的 class 不一致
const setThemePreference = (value: "light" | "dark" | "system") => {
  colorMode.preference = value;
  hideTooltip();
};

const toggleTheme = () => {
  colorMode.preference = isDark.value ? "light" : "dark";
  hideTooltip();
};

onMounted(() => {
  mounted.value = true;
  updateDockUnit();
  updateTime();
  timer = setInterval(updateTime, 1000);
  document.addEventListener("click", closePanels);
  window.addEventListener("resize", updateDockUnit, { passive: true });
});

onUnmounted(() => {
  clearInterval(timer);
  document.removeEventListener("click", closePanels);
  window.removeEventListener("resize", updateDockUnit);
});
</script>

<style scoped>
/* ------------------------------------------------------------
   主题变量：dock 自带一层玻璃，颜色只跟随 html.dark，
   不再用 @media(prefers-color-scheme) —— 站点是手动切主题的，
   媒体查询在"系统亮/站点暗"时会把文字刷成看不见的浅色。
   ------------------------------------------------------------ */
.warm-os-container {
  /* 缩放单位：1440×900 时 = 1px，按视口等比放大（4K = 2.4px） */
  --dk-u: clamp(1px, min(calc(100vw / 1440), calc(100vh / 900)), 3px);
  --dk-ink: #14120f;
  --dk-ink-2: rgba(20, 18, 15, 0.64);
  --dk-mute: rgba(20, 18, 15, 0.46);
  --dk-line: rgba(20, 18, 15, 0.14);
  --dk-hover: rgba(20, 18, 15, 0.06);
  --dk-active: rgba(20, 18, 15, 0.1);
  --dk-item: rgba(255, 255, 255, 0.5);
  --dk-item-strong: rgba(255, 255, 255, 0.86);
  /* 跟原版液态玻璃一致：只上一层很淡的白，靠折射层出效果 */
  --dk-glass: rgba(255, 255, 255, 0.2);
  --dk-gloss: rgba(255, 255, 255, 0.55);
  --dk-gloss-soft: rgba(255, 255, 255, 0.22);
  --dk-shadow: 0 calc(12 * var(--dk-u)) calc(32 * var(--dk-u))
    rgba(20, 18, 15, 0.14);
  --dk-tip-bg: rgba(20, 18, 15, 0.9);
  --dk-tip-ink: #fdfbf6;

  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 0;
  z-index: 100;
  pointer-events: none; /* 允许鼠标穿透到底层页面 */
}

html.dark .warm-os-container {
  --dk-ink: #f3f1ec;
  --dk-ink-2: rgba(243, 241, 236, 0.68);
  --dk-mute: rgba(243, 241, 236, 0.46);
  --dk-line: rgba(255, 255, 255, 0.16);
  --dk-hover: rgba(255, 255, 255, 0.09);
  --dk-active: rgba(255, 255, 255, 0.15);
  --dk-item: rgba(255, 255, 255, 0.08);
  --dk-item-strong: rgba(255, 255, 255, 0.18);
  --dk-glass: rgba(18, 19, 24, 0.45);
  --dk-gloss: rgba(255, 255, 255, 0.16);
  --dk-gloss-soft: rgba(255, 255, 255, 0.06);
  --dk-shadow: 0 calc(16 * var(--dk-u)) calc(40 * var(--dk-u))
    rgba(0, 0, 0, 0.55);
  --dk-tip-bg: rgba(245, 243, 238, 0.94);
  --dk-tip-ink: #14120f;
}

/* Tooltip 不在溢出隐藏容器内，自由设定位置和淡入动画 */
.global-tooltip {
  position: fixed;
  background-color: var(--dk-tip-bg);
  color: var(--dk-tip-ink);
  font-size: calc(12 * var(--dk-u));
  padding: calc(4 * var(--dk-u)) calc(10 * var(--dk-u));
  border-radius: calc(6 * var(--dk-u));
  pointer-events: none;
  opacity: 0;
  transform: translateX(-50%) translateY(calc(8 * var(--dk-u)));
  transition:
    opacity 0.2s cubic-bezier(0.34, 1.56, 0.64, 1),
    transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 1000;
  white-space: nowrap;
  box-shadow: var(--dk-shadow);
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
  max-width: calc(820 * var(--dk-u));
  height: calc(100 * var(--dk-u));
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: calc(24 * var(--dk-u)); /* 离底部的距离 */
  pointer-events: auto; /* 恢复交互 */
}

/* ================= 核心结构 ================= */
.island-wrapper {
  position: relative;
  transition:
    max-width 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
    height 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
    transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
  box-shadow:
    var(--dk-shadow),
    inset 0 calc(1 * var(--dk-u)) calc(1 * var(--dk-u)) var(--dk-gloss);
  border-radius: calc(24 * var(--dk-u));
}

/* 玻璃层贴合并占据所有体积 */
.island-glass {
  width: 100%;
  height: 100%;
  border-radius: inherit;
  transition: border-radius 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

/* 保留液态玻璃自己的折射层，只把高光/描边换成主题色 */
.island-glass :deep(.liquid_glass-sharp) {
  box-shadow:
    inset calc(1 * var(--dk-u)) calc(1 * var(--dk-u)) 0 0 var(--dk-gloss),
    inset calc(-1 * var(--dk-u)) calc(-1 * var(--dk-u)) 0 0 var(--dk-gloss);
}

.island-glass :deep(.liquid_glass-reflect) {
  box-shadow:
    inset calc(2 * var(--dk-u)) calc(2 * var(--dk-u)) calc(6 * var(--dk-u))
      calc(2 * var(--dk-u)) var(--dk-gloss-soft),
    inset calc(-2 * var(--dk-u)) calc(-2 * var(--dk-u)) calc(4 * var(--dk-u))
      calc(-1 * var(--dk-u)) var(--dk-gloss-soft);
}

/* == 状态尺码控制 == */
.island-wrapper.pill {
  max-width: calc(170 * var(--dk-u));
  height: calc(48 * var(--dk-u));
  transform: translateY(calc(4 * var(--dk-u))) scale(0.96);
  border-radius: calc(24 * var(--dk-u));
}

.island-wrapper.dock {
  max-width: calc(800 * var(--dk-u));
  height: calc(60 * var(--dk-u));
  transform: translateY(0) scale(1);
  border-radius: calc(28 * var(--dk-u));
}

.island-wrapper.menu {
  max-width: calc(800 * var(--dk-u));
  height: calc(480 * var(--dk-u));
  transform: translateY(0) scale(1);
  border-radius: calc(32 * var(--dk-u));
}

.island-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: max-content; /* 由内部内容驱动容器实际宽度 */
  height: 100%;
  margin: 0 auto;
}

/* ======== 第一层：状态栏 (Pill) ======== */
.island-status {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(48 * var(--dk-u));
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 calc(14 * var(--dk-u));
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
  gap: calc(8 * var(--dk-u));
  padding: calc(4 * var(--dk-u)) calc(8 * var(--dk-u));
  margin-left: calc(-8 * var(--dk-u));
  border-radius: calc(6 * var(--dk-u));
  cursor: pointer;
  transition: background-color 0.2s;
  overflow: hidden;
  white-space: nowrap;
}
.status-left:hover {
  background-color: var(--dk-hover);
}

.status-icon {
  color: var(--dk-ink-2);
  font-size: calc(14 * var(--dk-u));
}
.status-text {
  font-size: calc(13 * var(--dk-u));
  font-weight: 500;
  color: var(--dk-ink);
  max-width: calc(80 * var(--dk-u));
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.status-right {
  font-size: calc(12 * var(--dk-u));
  font-weight: 600;
  color: var(--dk-ink-2);
  cursor: pointer;
  padding: calc(4 * var(--dk-u)) calc(8 * var(--dk-u));
  margin-right: calc(-8 * var(--dk-u));
  border-radius: calc(6 * var(--dk-u));
  transition: background-color 0.2s;
}
.status-right:hover {
  background-color: var(--dk-hover);
}

/* ======== 第二层：主导航菜单 (Menu) ======== */
.island-menu {
  width: calc(360 * var(--dk-u));
  margin: 0 auto;
  opacity: 0;
  pointer-events: none;
  transform: translateY(calc(20 * var(--dk-u))) scale(0.95);
  transition:
    opacity 0.3s ease,
    transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  flex-direction: column;
  flex: 1; /* 撑满纵向高度，压住底部的 Dock */
  overflow: hidden;
}
.island-menu.show {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
}

.menu-spacer {
  height: calc(24 * var(--dk-u));
}

.search-box-wrapper {
  margin-bottom: calc(16 * var(--dk-u));
  padding: 0 calc(16 * var(--dk-u));
}
.search-box {
  display: flex;
  align-items: center;
  background: var(--dk-item);
  border-radius: calc(20 * var(--dk-u));
  padding: calc(8 * var(--dk-u)) calc(16 * var(--dk-u));
  box-shadow:
    inset 0 calc(2 * var(--dk-u)) calc(8 * var(--dk-u)) rgba(0, 0, 0, 0.06),
    0 calc(1 * var(--dk-u)) 0 var(--dk-gloss);
}
.search-icon {
  color: var(--dk-mute);
  margin-right: calc(8 * var(--dk-u));
}
.search-input {
  border: none;
  background: transparent;
  outline: none;
  flex: 1;
  font-size: calc(14 * var(--dk-u));
  color: var(--dk-ink);
}
.search-input::placeholder {
  color: var(--dk-mute);
}

.start-content {
  padding: 0 calc(24 * var(--dk-u)) calc(18 * var(--dk-u));
  flex: 1;
  display: flex;
  flex-direction: column;
}
.section-title {
  font-size: calc(13 * var(--dk-u));
  font-weight: 600;
  color: var(--dk-mute);
  margin-bottom: calc(12 * var(--dk-u));
  padding-left: calc(4 * var(--dk-u));
}
.mt-4 {
  margin-top: calc(16 * var(--dk-u));
}

.nav-panel-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  row-gap: calc(20 * var(--dk-u));
  column-gap: calc(16 * var(--dk-u));
  justify-items: center;
}
.nav-grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: var(--dk-ink);
  width: 100%;
  transition: transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.nav-grid-item:hover {
  transform: scale(1.05);
}

.nav-grid-item .icon-wrapper {
  width: calc(48 * var(--dk-u));
  height: calc(48 * var(--dk-u));
  border-radius: calc(12 * var(--dk-u));
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--dk-item);
  box-shadow: 0 calc(2 * var(--dk-u)) calc(8 * var(--dk-u)) rgba(0, 0, 0, 0.08);
  margin-bottom: calc(8 * var(--dk-u));
  color: var(--dk-ink-2);
  transition: background-color 0.2s;
}
.nav-grid-item:hover .icon-wrapper {
  background-color: var(--dk-item-strong);
}
.nav-grid-item.active .icon-wrapper {
  background-color: var(--cx-accent);
  color: var(--cx-accent-ink);
}
.nav-grid-item span {
  font-size: calc(12 * var(--dk-u));
  font-weight: 500;
}

/* ======== 外观（颜色模式） ======== */
.theme-segment {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: calc(6 * var(--dk-u));
  padding: calc(4 * var(--dk-u));
  border-radius: calc(14 * var(--dk-u));
  background: var(--dk-item);
}
.theme-option {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: calc(6 * var(--dk-u));
  height: calc(34 * var(--dk-u));
  padding: 0 calc(6 * var(--dk-u));
  border: 0;
  border-radius: calc(10 * var(--dk-u));
  background: transparent;
  color: var(--dk-ink-2);
  font-size: calc(12 * var(--dk-u));
  font-weight: 600;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}
.theme-option:hover {
  color: var(--dk-ink);
  background: var(--dk-hover);
}
.theme-option.active {
  background: var(--cx-accent);
  color: var(--cx-accent-ink);
}
.theme-option:focus-visible {
  outline: calc(2 * var(--dk-u)) solid var(--cx-accent);
  outline-offset: calc(2 * var(--dk-u));
}

/* ======== 第三层：应用底座 (Dock) ======== */
.island-dock {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: calc(6 * var(--dk-u));
  padding: calc(8 * var(--dk-u)) calc(12 * var(--dk-u));
  opacity: 0;
  transform: translateY(calc(10 * var(--dk-u))) scale(0.9);
  pointer-events: none;
  transition:
    opacity 0.3s ease,
    transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 10;
  height: calc(60 * var(--dk-u));
  flex-shrink: 0;
}
.island-dock.show {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
  transition:
    opacity 0.35s ease 0.15s,
    transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s;
}

.dock-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(44 * var(--dk-u));
  height: calc(44 * var(--dk-u));
  border-radius: calc(14 * var(--dk-u));
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}
.dock-icon {
  color: var(--dk-ink-2);
  transition: color 0.3s ease;
}

.dock-item:hover {
  background-color: var(--dk-hover);
  transform: translateY(calc(-6 * var(--dk-u)));
}
.dock-item.active {
  background-color: var(--dk-item-strong);
  transform: scale(1.1);
  box-shadow: 0 calc(2 * var(--dk-u)) calc(8 * var(--dk-u)) rgba(0, 0, 0, 0.12);
}

.divider {
  width: calc(1 * var(--dk-u));
  height: calc(28 * var(--dk-u));
  background-color: var(--dk-line);
  margin: 0 calc(2 * var(--dk-u));
  border-radius: calc(1 * var(--dk-u));
}

.dock-theme-icon {
  position: absolute;
}

.dock-theme-moon {
  display: inline-block;
}

.dock-theme-sun {
  display: none;
}

.dock-time-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 calc(10 * var(--dk-u));
  height: calc(44 * var(--dk-u));
  border-radius: calc(12 * var(--dk-u));
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  flex-shrink: 0;
}
.dock-time-widget:hover {
  background-color: var(--dk-hover);
}
.time-main {
  font-size: calc(13 * var(--dk-u));
  font-weight: 700;
  color: var(--dk-ink);
}
.time-sub {
  font-size: calc(10 * var(--dk-u));
  color: var(--dk-mute);
  margin-top: calc(-2 * var(--dk-u));
}
</style>

<style>
html.dark .dock-theme-moon {
  display: none;
}

html.dark .dock-theme-sun {
  display: inline-block;
}
</style>
