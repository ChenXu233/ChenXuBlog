<template>
  <div class="warm-os-container">
    <!-- 全局 Tooltip -->
    <div
      class="global-tooltip"
      :class="{ show: activeTooltip }"
      :style="tooltipStyle"
    >
      {{ activeTooltip }}
    </div>

    <!-- 系统面板（时钟/状态） -->
    <div v-if="showPanel" class="system-panel" @click.stop>
      <div class="panel-row">
        <UIcon name="i-heroicons-clock" class="w-4 h-4" />
        <span>{{ currentTime }}</span>
      </div>
      <div class="panel-row">
        <UIcon name="i-heroicons-calendar-days" class="w-4 h-4" />
        <span>{{ currentDate }}</span>
      </div>
      <div class="panel-row">
        <UIcon name="i-heroicons-bolt" class="w-4 h-4" />
        <span>FPS {{ fps }}</span>
      </div>
    </div>

    <div
      class="nav-trigger-area"
      @mouseenter="isHovered = true"
      @mouseleave="isHovered = false"
    >
      <div class="island-wrapper" :class="viewState">
        <!-- 收缩态：状态条 -->
        <div
          class="island-status"
          :class="{ hide: viewState !== 'pill' }"
          @click.stop="toggleNavPanel"
        >
          <div class="status-left">
            <UIcon :name="currentIcon" class="status-icon" />
            <span class="status-text">{{ currentMenuName }}</span>
          </div>
          <div class="status-right" @click.stop="toggleSystemPanel">
            {{ timeShort }}
          </div>
        </div>

        <!-- 展开态：Dock -->
        <div class="island-dock" :class="{ show: viewState !== 'pill' }">
          <div
            class="dock-item"
            :class="{ active: showNavPanel }"
            @click.stop="toggleNavPanel"
            @mouseenter="showTooltip($event, '主菜单')"
            @mouseleave="hideTooltip"
          >
            <UIcon name="i-heroicons-squares-2x2" class="dock-icon" />
          </div>
          <div class="divider"></div>

          <NuxtLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="dock-item"
            :class="{ active: route.path.startsWith(item.path) }"
            @mouseenter="showTooltip($event, item.name)"
            @mouseleave="hideTooltip"
          >
            <UIcon :name="item.icon" class="dock-icon" />
          </NuxtLink>

          <div class="divider"></div>
          <div class="dock-fps-widget">
            <span class="fps-value" :style="{ color: fpsColor }">{{
              fps
            }}</span>
            <span class="fps-label">FPS</span>
          </div>
          <div class="divider"></div>
          <div class="dock-time-widget" @click.stop="toggleSystemPanel">
            <span class="time-main">{{ timeShort }}</span>
            <span class="time-sub">{{ dateShort }}</span>
          </div>
        </div>

        <!-- 二次展开：开始菜单 -->
        <div class="island-menu" :class="{ show: viewState === 'menu' }">
          <div class="menu-spacer"></div>
          <div class="user-panel">
            <NuxtLink
              :to="
                auth.isAuthenticated
                  ? `/user/${auth.user?.uuid || ''}`
                  : '/login?redirect=' + route.fullPath
              "
              class="user-card"
              @click="closePanels"
            >
              <div class="user-card-avatar-shell">
                <img
                  :src="
                    auth.user?.avatar ||
                    'https://avatars.githubusercontent.com/u/91937041?v=4'
                  "
                  :alt="auth.user?.username || '访客'"
                  class="user-card-avatar"
                />
                <span
                  class="user-card-status"
                  :class="{ active: auth.isAuthenticated }"
                ></span>
              </div>
              <div class="user-card-copy">
                <span class="user-card-kicker">{{
                  auth.isAuthenticated ? "个人空间" : "欢迎回来"
                }}</span>
                <span class="user-card-title">{{
                  auth.isAuthenticated ? auth.user?.username : "登录 ChenXuBlog"
                }}</span>
                <span class="user-card-meta">{{
                  auth.isAuthenticated
                    ? "进入个人主页与账户设置"
                    : "登录后同步头像与资料"
                }}</span>
              </div>
              <UButton
                v-if="auth.isAuthenticated"
                icon="i-heroicons-arrow-right-on-rectangle"
                size="xs"
                color="error"
                variant="ghost"
                @click.stop="handleLogout"
                >退出</UButton
              >
            </NuxtLink>
          </div>

          <div class="start-content">
            <div class="section-title">所有页面</div>
            <div class="nav-panel-grid">
              <NuxtLink
                v-for="item in allNavItems"
                :key="item.path"
                :to="item.path"
                class="nav-grid-item"
                :class="{ active: route.path.startsWith(item.path) }"
                @click="closePanels"
              >
                <div class="icon-wrapper">
                  <UIcon :name="item.icon" class="w-5 h-5" />
                </div>
                <span>{{ item.name }}</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";

const route = useRoute();
const auth = useAuthStore();

const isHovered = ref(false);
const showNavPanel = ref(false);
const showPanel = ref(false);
const activeTooltip = ref("");
const tooltipX = ref(0);
const tooltipY = ref(0);

const viewState = computed(() => {
  if (showNavPanel.value) return "menu";
  if (isHovered.value) return "dock";
  return "pill";
});

const tooltipStyle = computed(() => ({
  left: tooltipX.value + "px",
  bottom: tooltipY.value + "px",
}));

const showTooltip = (e: MouseEvent, text: string) => {
  activeTooltip.value = text;
  const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
  tooltipX.value = rect.left + rect.width / 2;
  tooltipY.value = window.innerHeight - rect.top + 8;
};
const hideTooltip = () => (activeTooltip.value = "");

const toggleNavPanel = () => {
  showNavPanel.value = !showNavPanel.value;
  if (showNavPanel.value) showPanel.value = false;
};
const toggleSystemPanel = () => {
  showPanel.value = !showPanel.value;
  if (showPanel.value) showNavPanel.value = false;
};
const closePanels = () => {
  showPanel.value = false;
  showNavPanel.value = false;
};

const navItems = [
  { name: "首页", path: "/home", icon: "i-heroicons-home" },
  { name: "文章", path: "/article", icon: "i-heroicons-document-text" },
  { name: "归档", path: "/archive", icon: "i-heroicons-archive-box" },
  { name: "随谈", path: "/diary", icon: "i-heroicons-chat-bubble-left-right" },
  { name: "友链", path: "/friend", icon: "i-heroicons-user-group" },
  { name: "WarmOS", path: "/warmos", icon: "i-heroicons-computer-desktop" },
];

const allNavItems = computed(() => {
  const items = [...navItems];
  if (auth.isAdmin)
    items.push({
      name: "管理后台",
      path: "/admin",
      icon: "i-heroicons-cog-6-tooth",
    });
  return items;
});

const currentMenuName = computed(
  () =>
    allNavItems.value.find(
      (i) => route.path.startsWith(i.path) && i.path !== "/home",
    )?.name || "首页",
);
const currentIcon = computed(
  () =>
    allNavItems.value.find(
      (i) => route.path.startsWith(i.path) && i.path !== "/home",
    )?.icon || "i-heroicons-home",
);

const now = ref(new Date());
let timer: ReturnType<typeof setInterval>;
const timeShort = computed(() =>
  now.value.toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" }),
);
const dateShort = computed(() =>
  now.value.toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" }),
);
const currentTime = computed(() => now.value.toLocaleTimeString("zh-CN"));
const currentDate = computed(() =>
  now.value.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }),
);

const fps = ref(0);
let frameCount = 0;
let lastFrame = performance.now();
let fpsId: number;
const fpsColor = computed(() =>
  fps.value >= 45 ? "#10b981" : fps.value >= 30 ? "#f59e0b" : "#ef4444",
);

const calcFps = () => {
  const t = performance.now();
  frameCount++;
  if (t - lastFrame >= 1000) {
    fps.value = Math.round((frameCount * 1000) / (t - lastFrame));
    frameCount = 0;
    lastFrame = t;
  }
  fpsId = requestAnimationFrame(calcFps);
};

const handleLogout = () => {
  auth.logout();
  closePanels();
};

onMounted(() => {
  timer = setInterval(() => (now.value = new Date()), 1000);
  fpsId = requestAnimationFrame(calcFps);
  document.addEventListener("click", closePanels);
});
onUnmounted(() => {
  clearInterval(timer);
  cancelAnimationFrame(fpsId);
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
  pointer-events: none;
}

.global-tooltip {
  position: fixed;
  background: rgba(0, 0, 0, 0.75);
  color: #fff;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
  opacity: 0;
  transform: translateX(-50%) translateY(8px);
  transition:
    opacity 0.2s,
    transform 0.2s;
  z-index: 1000;
  white-space: nowrap;
}
.global-tooltip.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.system-panel {
  position: fixed;
  right: 20px;
  bottom: 90px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  pointer-events: auto;
  color: #333;
  font-size: 13px;
}
.panel-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
@media (prefers-color-scheme: dark) {
  .system-panel {
    background: rgba(30, 40, 55, 0.9);
    color: #eee;
    border-color: rgba(255, 255, 255, 0.08);
  }
}

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
  padding-bottom: 24px;
  pointer-events: auto;
}

.island-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
  box-shadow:
    0 12px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 1px rgba(255, 255, 255, 0.6);
  border-radius: 24px;
  transition:
    max-width 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
    height 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
    transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.island-wrapper.pill {
  max-width: 170px;
  height: 48px;
  transform: translateY(4px) scale(0.96);
  border-radius: 24px;
}
.island-wrapper.dock {
  max-width: 560px;
  height: 60px;
  transform: translateY(0) scale(1);
  border-radius: 28px;
}
.island-wrapper.menu {
  max-width: 480px;
  height: 480px;
  transform: translateY(0) scale(1);
  border-radius: 34px;
}

.island-status {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 48px;
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
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
}
.status-left:hover {
  background: rgba(0, 0, 0, 0.05);
}
.status-icon {
  width: 14px;
  height: 14px;
  color: #555;
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
  padding: 4px 8px;
  border-radius: 6px;
  cursor: pointer;
}

.island-dock {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  opacity: 0;
  transform: translateY(10px) scale(0.9);
  pointer-events: none;
  transition:
    opacity 0.3s ease,
    transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 10;
  height: 44px;
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
  width: 44px;
  height: 44px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
  text-decoration: none;
}
.dock-icon {
  width: 20px;
  height: 20px;
  color: #444;
}
.dock-item:hover {
  background: rgba(255, 255, 255, 0.6);
  transform: translateY(-6px);
}
.dock-item.active {
  background: rgba(255, 255, 255, 0.8);
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.divider {
  width: 1px;
  height: 28px;
  background: rgba(0, 0, 0, 0.15);
  margin: 0 2px;
  border-radius: 1px;
}

.dock-fps-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 8px;
  height: 44px;
  flex-shrink: 0;
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

.dock-time-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 10px;
  height: 44px;
  border-radius: 12px;
  cursor: pointer;
  flex-shrink: 0;
}
.dock-time-widget:hover {
  background: rgba(0, 0, 0, 0.05);
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

.island-menu {
  width: 100%;
  margin: 0 auto;
  opacity: 0;
  pointer-events: none;
  transform: translateY(20px) scale(0.95);
  transition:
    opacity 0.3s ease,
    transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
.island-menu.show {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
}

.menu-spacer {
  height: 20px;
}
.user-panel {
  padding: 0 20px 16px;
  position: relative;
  z-index: 10;
  pointer-events: auto;
}
.user-card {
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 72px;
  padding: 14px 16px;
  border-radius: 20px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.5),
    rgba(244, 248, 255, 0.62)
  );
  text-decoration: none;
  transition:
    transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.28s ease;
}
.user-card:hover {
  transform: translateY(-3px) scale(1.015);
  box-shadow: 0 18px 34px rgba(15, 23, 42, 0.16);
}
.user-card-avatar-shell {
  flex-shrink: 0;
  width: 52px;
  height: 52px;
  border-radius: 18px;
  padding: 2px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.95),
    rgba(170, 204, 255, 0.58)
  );
}
.user-card-avatar {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  object-fit: cover;
}
.user-card-status {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(148, 163, 184, 0.95);
  border: 2px solid #fff;
}
.user-card-status.active {
  background: #34c759;
}
.user-card-copy {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.user-card-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(74, 85, 104, 0.72);
}
.user-card-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 17px;
  font-weight: 700;
  color: #1f2937;
}
.user-card-meta {
  font-size: 12px;
  color: rgba(55, 65, 81, 0.72);
}

.start-content {
  padding: 0 24px 10px;
  flex: 1;
  overflow-y: auto;
}
.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-bottom: 14px;
  padding-left: 4px;
}
.nav-panel-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  row-gap: 20px;
  column-gap: 14px;
  justify-items: center;
}
.nav-grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #333;
  width: 100%;
  transition: transform 0.2s;
  position: relative;
  z-index: 10;
  cursor: pointer;
}
.nav-grid-item:hover {
  transform: scale(1.05);
}
.nav-grid-item .icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 8px;
  color: #555;
}
.nav-grid-item.active .icon-wrapper {
  background: #f4b3c2;
  color: #fff;
}
.nav-grid-item span {
  font-size: 12px;
  font-weight: 500;
}

@media (prefers-color-scheme: dark) {
  .island-wrapper {
    box-shadow:
      0 12px 32px rgba(0, 0, 0, 0.4),
      inset 0 1px 1px rgba(255, 255, 255, 0.1);
  }
  .dock-icon {
    color: #ddd;
  }
  .dock-item:hover {
    background: rgba(255, 255, 255, 0.15);
  }
  .dock-item.active {
    background: rgba(255, 255, 255, 0.25);
  }
  .time-main,
  .status-text {
    color: #eee;
  }
  .status-icon,
  .time-sub,
  .fps-label,
  .status-right {
    color: #aaa;
  }
  .divider {
    background: rgba(255, 255, 255, 0.2);
  }
  .user-card {
    background: linear-gradient(
      135deg,
      rgba(35, 43, 56, 0.94),
      rgba(20, 27, 38, 0.82)
    );
  }
  .user-card-title {
    color: #f8fafc;
  }
  .user-card-kicker {
    color: rgba(203, 213, 225, 0.62);
  }
  .user-card-meta {
    color: rgba(226, 232, 240, 0.7);
  }
  .section-title {
    color: #aaa;
  }
  .nav-grid-item {
    color: #eee;
  }
  .nav-grid-item .icon-wrapper {
    background: rgba(255, 255, 255, 0.1);
    color: #ddd;
  }
  .nav-grid-item.active .icon-wrapper {
    background: #b0637e;
    color: #fff;
  }
}
</style>
