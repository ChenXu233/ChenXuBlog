<template>
  <div class="warm-os-desktop">
    <!-- Desktop Background -->
    <div class="desktop-wallpaper"></div>

    <!-- Render all open windows -->
    <Window
      v-for="app in openApps"
      :key="app.id"
      v-show="!app.minimized"
      :app="app"
      :zIndex="getBaseZIndex(app.id)"
      @close="closeApp"
      @minimize="minimizeApp"
      @focus="focusApp(app.id)"
    />

    <!-- Desktop Icons (Basic) -->
    <div class="desktop-icons">
      <div
        class="desktop-icon"
        v-for="app in defaultApps"
        :key="app.id"
        @dblclick="openApp(app)"
      >
        <div class="icon-img-wrapper">
          <i :class="['fa', app.icon, 'text-3xl']"></i>
        </div>
        <span class="icon-label">{{ app.title }}</span>
      </div>
    </div>

    <!-- Dockbar from original project -->
    <DockBar class="warm-dock" />
  </div>
</template>

<script setup lang="ts">
import { ref, shallowRef } from "vue";
import Window from "@/components/WarmOS/Window.vue";
import DockBar from "@/components/WarmOS/DockBar.vue";
import BrowserApp from "@/components/WarmOS/Apps/browser/index.vue";
import TerminalApp from "@/components/WarmOS/Apps/terminal/index.vue";
import {
  openApps,
  openApp,
  closeApp,
  minimizeApp,
  focusApp,
  getBaseZIndex,
  type AppConfig,
} from "@/stores/warmos";

// Available Apps on Desktop
const defaultApps = ref<AppConfig[]>([
  {
    id: "app-blog",
    title: "博客前台",
    icon: "fa-globe",
    type: "iframe",
    url: "/", // Points to the root vue router path
    defaultWidth: 1000,
    defaultHeight: 700,
    defaultX: 100,
    defaultY: 50,
  },
  {
    id: "app-terminal",
    title: "终端",
    icon: "fa-terminal",
    type: "component",
    component: shallowRef(TerminalApp),
    defaultWidth: 600,
    defaultHeight: 450,
    defaultX: 200,
    defaultY: 150,
  },
  {
    id: "app-browser",
    title: "浏览器",
    icon: "fa-edge",
    type: "component",
    component: shallowRef(BrowserApp),
    props: { url: "https://www.wikipedia.org" },
    defaultWidth: 1000,
    defaultHeight: 650,
    defaultX: 150,
    defaultY: 100,
  },
  {
    id: "app-admin",
    title: "系统管理",
    icon: "fa-cogs",
    type: "iframe",
    url: "/admin", // Points to another path (optional)
    defaultWidth: 900,
    defaultHeight: 600,
    defaultX: 150,
    defaultY: 80,
  },
]);
</script>

<style scoped>
.warm-os-desktop {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.desktop-wallpaper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("https://images.unsplash.com/photo-1579546929518-9e396f3cc809?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80")
    center/cover no-repeat;
  z-index: -1;
}

/* Desktop Icons */
.desktop-icons {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 1;
}

.desktop-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: white;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.desktop-icon:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.icon-img-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.icon-label {
  font-size: 12px;
  text-align: center;
  word-break: break-word;
}

/* Taskbar */
.warm-os-taskbar {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 48px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 9999;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.taskbar-content {
  display: flex;
  gap: 10px;
}

.taskbar-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: white;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  min-width: 120px;
  max-width: 160px;
  user-select: none;
}

.taskbar-item:hover {
  background: rgba(255, 255, 255, 0.2);
}

.taskbar-item.active {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.taskbar-item.minimized {
  opacity: 0.7;
}

.item-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
