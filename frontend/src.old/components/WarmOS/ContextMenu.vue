<template>
  <Teleport to="body">
    <Transition name="fade-scale">
      <div
        v-if="visible"
        class="context-menu-wrapper"
        :style="{ left: x + 'px', top: y + 'px' }"
        @click.stop
        @contextmenu.prevent.stop
      >
        <LiquidGlass border-radius="8px" bg-color="rgba(255, 255, 255, 0.4)">
          <div class="context-menu-content">
            <template v-for="(item, index) in items" :key="index">
              <div v-if="item.separator" class="menu-separator"></div>
              <div
                v-else
                class="context-menu-item"
                :class="item.class"
                :style="{ color: item.color }"
                @click="handleAction(item)"
              >
                <i v-if="item.icon" :class="['fa', item.icon, 'item-icon']"></i>
                <span>{{ item.label }}</span>
              </div>
            </template>
          </div>
        </LiquidGlass>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import LiquidGlass from '@/components/LiquidGlass.vue'

export interface MenuItem {
  label?: string
  icon?: string
  action?: () => void
  class?: string | string[] | Record<string, boolean>
  color?: string
  separator?: boolean
}

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  x: {
    type: Number,
    default: 0
  },
  y: {
    type: Number,
    default: 0
  },
  items: {
    type: Array as () => MenuItem[],
    default: () => []
  }
})

const emit = defineEmits(['update:visible'])

const handleAction = (item: MenuItem) => {
  if (item.action) {
    item.action()
  }
  emit('update:visible', false)
}

const handleClickOutside = () => {
  if (props.visible) {
    emit('update:visible', false)
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('contextmenu', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('contextmenu', handleClickOutside)
})
</script>

<style scoped>
/* 全局右键菜单 */
.context-menu-wrapper {
  position: fixed;
  border-radius: 8px;
  min-width: 140px;
  z-index: 9999;
  transform: translateY(-100%);
  user-select: none;
}

.context-menu-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 4px;
}

.context-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  font-size: 13px;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
}
.context-menu-item:hover {
  background: rgba(0, 0, 0, 0.05);
}
.item-icon {
  width: 14px;
  text-align: center;
}
.menu-separator {
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
  margin: 4px 0;
}

/* 动画 */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: translateY(-90%) scale(0.95);
}
</style>
