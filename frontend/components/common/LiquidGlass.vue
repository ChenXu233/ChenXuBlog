<template>
  <div
    class="liquid_glass-wrapper"
    :style="{
      '--border-radius': borderRadius || '16px',
      '--bg-color': bgColor || 'rgba(0, 0, 0, 0.12)',
      '--glass-u': scale + 'px',
    }"
  >
    <!-- SVG Filter Definition（每个实例一个独立 id，位移量才能各自缩放） -->
    <svg style="display: none">
      <defs>
        <filter
          :id="filterId"
          x="0%"
          y="0%"
          width="100%"
          height="100%"
          filterUnits="objectBoundingBox"
        >
          <feDisplacementMap :scale="200 * scale" />
        </filter>
      </defs>
    </svg>

    <!-- Layers -->
    <div
      class="liquid_glass-outer"
      :style="{
        backdropFilter: `url(#${filterId})`,
        WebkitBackdropFilter: `url(#${filterId})`,
        maskImage: outerMask,
        WebkitMaskImage: outerMask,
      }"
    ></div>
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
import { computed, useId } from "vue";

const props = withDefaults(
  defineProps<{
    borderRadius?: string;
    bgColor?: string;
    /**
     * 玻璃几何的缩放系数，1 = 原始 16px 基准。
     * 折射环厚度、内框圆角、位移量、高光描边都按它等比放大，
     * 否则 4K 下外环还是 5px、圆角还是 21px，液态玻璃就散架了。
     */
    scale?: number;
  }>(),
  { scale: 1 },
);

const uid = useId();
const filterId = `liquid_glass_filter_${uid}`;

const safeScale = computed(() =>
  Number.isFinite(props.scale) && props.scale > 0 ? props.scale : 1,
);

/** 外环厚度（原版 5px） */
const ring = computed(() => round(5 * safeScale.value));
/** 内框圆角（原版 21px） */
const innerRadius = computed(() => round(21 * safeScale.value));

const outerMask = computed(() => {
  const r = ring.value;
  const rx = innerRadius.value;
  const inner =
    "<rect x='" +
    r +
    "' y='" +
    r +
    "' width='calc(100% - " +
    r * 2 +
    "px)' height='calc(100% - " +
    r * 2 +
    "px)' rx='" +
    rx +
    "' ry='" +
    rx +
    "' fill='white'/>";
  return [
    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'><rect x='0' y='0' width='100%' height='100%' fill='white'/></svg>\")",
    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'>" +
      inner +
      '</svg>")',
  ].join(", ");
});

function round(n: number) {
  return Math.round(n * 100) / 100;
}
</script>

<style scoped>
.liquid_glass-wrapper {
  position: relative;
  display: flex;
  border-radius: var(--border-radius, 16px);
}

/* 确保背景层有自己的 overflow: hidden 等来切除圆角外框 */
.liquid_glass-outer {
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  overflow: hidden;
  /* backdrop-filter / mask-image 在脚本里按 scale 生成 */
  mask-composite: exclude;
  -webkit-mask-composite: xor;
}

.liquid_glass-cover {
  backdrop-filter: blur(calc(2 * var(--glass-u, 1px)));
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
    inset calc(1 * var(--glass-u, 1px)) calc(1 * var(--glass-u, 1px)) 0 0
      rgba(255, 255, 255, 0.5),
    inset calc(-1 * var(--glass-u, 1px)) calc(-1 * var(--glass-u, 1px)) 0 0
      rgba(255, 255, 255, 0.6);
  border-radius: var(--border-radius, 16px);
}

.liquid_glass-reflect {
  position: absolute;
  inset: calc(1 * var(--glass-u, 1px));
  z-index: 2;

  box-shadow:
    inset calc(2 * var(--glass-u, 1px)) calc(2 * var(--glass-u, 1px))
      calc(6 * var(--glass-u, 1px)) calc(2 * var(--glass-u, 1px))
      rgba(255, 255, 255, 0.2),
    inset calc(-2 * var(--glass-u, 1px)) calc(-2 * var(--glass-u, 1px))
      calc(4 * var(--glass-u, 1px)) calc(-1 * var(--glass-u, 1px))
      rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius, 16px);
}

.liquid_glass-content {
  position: relative;
  z-index: 4;
  width: 100%;
}
</style>
