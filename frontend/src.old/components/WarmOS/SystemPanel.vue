<template>
  <transition name="panel-fade">
    <LiquidGlass v-show="modelValue" class="system-panel" @click.stop bg-color="rgba(255, 255, 255, 0.2)"> >
      <div class="panel-header">
        <div class="panel-time">{{ currentTime }}</div>
        <div class="panel-date">{{ currentDate }}</div>
      </div>
      
      <div class="panel-body">
        <!-- 系统状态模块 -->
        <div class="system-stats">
          <div class="stat-item">
            <span class="stat-label">FPS</span>
            <span class="stat-value" :class="fpsColor">{{ fps }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">内存使用</span>
            <span class="stat-value">{{ memoryUsage }} MB</span>
          </div>
          <div class="stat-item ua-item">
            <span class="stat-label">环境</span>
            <span class="stat-value text-ellipsis" :title="ua">{{ ua }}</span>
          </div>
        </div>

        <!-- 简易日历 -->
        <div class="calendar-module">
          <div class="calendar-header">{{ currentYearMonth }}</div>
          <div class="calendar-grid">
            <div v-for="day in weekDays" :key="day" class="cal-day-header">{{ day }}</div>
            <div v-for="blank in firstDayOfWeek" :key="'b'+blank" class="cal-cell empty"></div>
            <div 
              v-for="d in daysInMonth" 
              :key="'d'+d" 
              class="cal-cell"
              :class="{ 'cal-today': d === currentDay }"
            >
              {{ d }}
            </div>
          </div>
        </div>
      </div>
    </LiquidGlass>
  </transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import LiquidGlass from '../LiquidGlass.vue'
const props = defineProps({
  modelValue: Boolean
})

// 时间和日期
const currentTime = ref('')
const currentDate = ref('')
const currentYearMonth = ref('')
const currentDay = ref(1)

const weekDays = ['日', '一', '二', '三', '四', '五', '六']
const daysInMonth = ref(30)
const firstDayOfWeek = ref(0) // 0是周日

const updateDateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  currentDate.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })
  currentYearMonth.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' })
  currentDay.value = now.getDate()
  
  // 日历计算
  const year = now.getFullYear()
  const month = now.getMonth()
  daysInMonth.value = new Date(year, month + 1, 0).getDate()
  firstDayOfWeek.value = new Date(year, month, 1).getDay()
}

// 帧率
const fps = ref(0)
let frameCount = 0
let lastTime = performance.now()
let rafId = 0

const measureFPS = () => {
  const now = performance.now()
  frameCount++
  if (now >= lastTime + 1000) {
    fps.value = Math.round((frameCount * 1000) / (now - lastTime))
    frameCount = 0
    lastTime = now
  }
  rafId = requestAnimationFrame(measureFPS)
}

const fpsColor = computed(() => {
  if (fps.value >= 50) return 'color-good'
  if (fps.value >= 30) return 'color-warn'
  return 'color-bad'
})

// 内存与环境
const memoryUsage = ref('0.00')
const ua = ref(navigator.userAgent)
let memTimer = 0

const updateMemory = () => {
  // 必须强制转换为any因为 performance.memory 是非标准api，存在于Chrome等
  const perf = performance as any
  if (perf && perf.memory) {
    memoryUsage.value = (perf.memory.usedJSHeapSize / (1024 * 1024)).toFixed(2)
  } else {
    memoryUsage.value = '不支持'
  }
}

watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    measureFPS()
    memTimer = window.setInterval(updateMemory, 1000)
  } else {
    cancelAnimationFrame(rafId)
    clearInterval(memTimer)
  }
})

let clockTimer = 0
onMounted(() => {
  updateDateTime()
  updateMemory()
  clockTimer = window.setInterval(updateDateTime, 1000)
})

onUnmounted(() => {
  clearInterval(clockTimer)
  clearInterval(memTimer)
  cancelAnimationFrame(rafId)
})
</script>

<style scoped>
.system-panel {
  position: absolute; /* 相对于 body 是 fixed, 这里用 absolute 和外层容器联动更好, 但我们要 fixed 方便定位 */
  position: fixed;
  bottom: 80px; /* 距离底部Dock的距离 */
  left: 50%;
  margin-left: 20px; /* Dock 大约一半宽度，时间在右侧，从中心偏移一点让它对齐 Dock 右沿 */
  width: 320px;
  border-radius: 12px;
  padding: 16px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 16px;
  cursor: default;
}

.panel-header {
  border-bottom: 1px solid rgba(128, 128, 128, 0.2);
  padding-bottom: 12px;
}

.panel-time {
  font-size: 28px;
  font-weight: 300;
  letter-spacing: -0.5px;
}

.panel-date {
  font-size: 13px;
  color: #0078d4;
  margin-top: 4px;
}

.system-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(128, 128, 128, 0.05);
  padding: 10px;
  border-radius: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.ua-item {
  flex-direction: column;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  font-size: 11px;
  color: #666;
  margin-top: 2px;
}

@media (prefers-color-scheme: dark) {
  .text-ellipsis {
    color: #aaa;
  }
}

.stat-label {
  color: #666;
}
@media (prefers-color-scheme: dark) {
  .stat-label { color: #aaa; }
}

.stat-value.color-good { color: #107c10; font-weight: bold; }
.stat-value.color-warn { color: #d83b01; font-weight: bold; }
.stat-value.color-bad { color: #a4262c; font-weight: bold; }

@media (prefers-color-scheme: dark) {
  .stat-value.color-good { color: #6ce26c; }
  .stat-value.color-warn { color: #ff8c00; }
  .stat-value.color-bad { color: #ff5f5f; }
}

/* 日历样式 */
.calendar-module {
  margin-top: 4px;
}

.calendar-header {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 12px;
  text-align: center;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  text-align: center;
}

.cal-day-header {
  font-size: 12px;
  font-weight: bold;
  color: #666;
  padding-bottom: 4px;
}

@media (prefers-color-scheme: dark) {
  .cal-day-header { color: #aaa; }
}

.cal-cell {
  font-size: 13px;
  width: 28px;
  height: 28px;
  line-height: 28px;
  margin: 0 auto;
  border-radius: 50%;
}

.cal-cell:not(.empty):hover {
  background: rgba(128, 128, 128, 0.2);
}

.cal-today {
  background: #0078d4;
  color: #fff;
  font-weight: bold;
}
.cal-today:hover {
  background: #005a9e !important;
}

/* Vue transition */
.panel-fade-enter-active,
.panel-fade-leave-active {
  transition: opacity 0.2s, transform 0.2s cubic-bezier(0.2, 0.9, 0.3, 1);
}
.panel-fade-enter-from,
.panel-fade-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.98);
}
</style>
