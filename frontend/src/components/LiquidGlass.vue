<template>
  <div
    class="liquid_glass-wrapper"
    :style="{ 
      '--border-radius': borderRadius || '16px',
      '--bg-color': bgColor || 'rgba(0, 0, 0, 0.12)'
    }"
  >
    <!-- SVG Filter Definition -->
    <svg style="display: none">
      <defs>
        <filter
          id="liquid_glass_filter"
          x="0%"
          y="0%"
          width="100%"
          height="100%"
          filterUnits="objectBoundingBox"
        >
          <feDisplacementMap scale="200" />
        </filter>
      </defs>
    </svg>

    <!-- Layers -->
    <div class="liquid_glass-outer"></div>
    <div class="liquid_glass-cover"></div>
    <div class="liquid_glass-sharp"></div>
    <div class="liquid_glass-reflect"></div>

    <!-- Content Slot -->
    <div class="liquid_glass-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  borderRadius?: string;
  bgColor?: string;
}>();
</script>

<style scoped>
.liquid_glass-wrapper {
  position: relative;
  display: flex;
  border-radius: var(--border-radius, 16px);
  /* overflow: hidden removed to allow tooltips to spill out */
}

/* 确保背景层有自己的 overflow: hidden 等来切除圆角外框 */
.liquid_glass-outer {
  backdrop-filter: url(#liquid_glass_filter);
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  overflow: hidden;

  mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><rect x="0" y="0" width="100%" height="100%" rx="0" ry="0" fill="white"/></svg>'),
    url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><rect x="5" y="5" width="calc(100% - 10px)" height="calc(100% - 10px)" rx="21" ry="21" fill="white"/></svg>');
  mask-composite: exclude;
}

.liquid_glass-cover {
  backdrop-filter: blur(2px);
  position: absolute;
  inset: 0;
  z-index: 2;
  border-radius: var(--border-radius, 16px);
  background: var(--bg-color);
}

.liquid_glass-sharp {
  position: absolute;
  inset: 0;
  z-index: 3;

  box-shadow:
    inset 1px 1px 0px 0px rgba(255, 255, 255, 0.5),
    inset -1px -1px 0px 0px rgba(255, 255, 255, 0.6);
  border-radius: var(--border-radius, 16px);
}

.liquid_glass-reflect {
  position: absolute;
  inset: 1px;
  z-index: 2;

  box-shadow:
    inset 2px 2px 6px 2px rgba(255, 255, 255, 0.2),
    inset -2px -2px 4px -1px rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius, 16px);
}

.liquid_glass-content {
  position: relative;
  z-index: 4;
  width: 100%;
}
</style>
