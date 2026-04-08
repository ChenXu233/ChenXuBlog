<template>
  <div class="bamboo-forest" ref="forestRef">
    <svg class="bamboo-svg" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="stalkGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#9db495" />
          <stop offset="40%" stop-color="#dce5d8" />
          <stop offset="60%" stop-color="#dce5d8" />
          <stop offset="100%" stop-color="#8fa486" />
        </linearGradient>
        <linearGradient id="leafGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#8fa486" />
          <stop offset="100%" stop-color="#b0c4a8" />
        </linearGradient>
      </defs>

      <g
        v-for="bamboo in bamboos"
        :key="bamboo.id"
        class="bamboo-group"
        :style="{ '--parallax-dist': bamboo.speed + 'px', opacity: bamboo.opacity }"
      >
        <!-- 主干替换为 Path 以支持下粗上细 -->
        <path :d="bamboo.trunkPath" fill="url(#stalkGrad)" />
        
        <!-- 竹壳/竹节 -->
        <rect
          v-for="(j, idx) in bamboo.joints"
          :key="'j'+idx"
          :x="bamboo.x - j.width / 2 - 2"
          :y="j.y"
          :width="j.width + 4"
          height="4"
          fill="#7a9073"
          rx="2"
        />

        <g v-for="(branch, bKey) in bamboo.branches" :key="'b'+bKey">
          <!-- 树枝茎干 -->
          <line
            :x1="branch.startX"
            :y1="branch.y"
            :x2="branch.endX"
            :y2="branch.endY"
            stroke="#7a9073"
            :stroke-width="branch.width"
          />
          <!-- 树叶 -->
          <g v-for="(leaf, lKey) in branch.leaves" :key="'l'+lKey" :transform="leaf.transform">
             <path d="M 0,0 Q 20,-10 40,0 Q 20,10 0,0 Z" fill="url(#leafGrad)" />
          </g>
        </g>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps<{ progress?: number }>();
const forestRef = ref<HTMLElement | null>(null);

function seed(s: number) {
  return function () {
    s = Math.sin(s) * 10000;
    return s - Math.floor(s);
  };
}

interface BambooJoint {
  y: number;
  width: number;
}

interface Bamboo {
  id: number;
  x: number;
  speed: number;
  opacity: number;
  zIndex: number;
  trunkPath: string;
  joints: BambooJoint[];
  branches: {
    startX: number;
    y: number;
    endX: number;
    endY: number;
    width: number;
    leaves: { transform: string }[];
  }[];
}

const bamboos = ref<Bamboo[]>([]);
let resizeObserver: ResizeObserver | null = null;
let debounceTimer: ReturnType<typeof setTimeout> | null = null;

function generateForest() {
  if (!forestRef.value) return;
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const containerHeight = forestRef.value.clientHeight;
  
  const generated: Bamboo[] = [];
  
  // 根据屏幕宽度动态推算竹子数量（保证1920px宽度下约为42根，移动端相应减少，最少10根）
  const bambooCount = Math.max(5, Math.floor(vw / 45));
  
  for (let i = 0; i < bambooCount; i++) {
    const rnd = seed(i+1145);
    const x = -vw * 0.1 + rnd() * (vw * 1.2);
    const zIndex = Math.floor(rnd() * 10);
    const baseWidth = 15 + (zIndex * 2.5) + rnd() * 20; 
    
    const speed = 200 + zIndex * 1000;
    
    // 恢复顶部齐平：所有竹子统一在这个高度的顶部起笔为 0
    const startY = 0.68 * vh; // 从视口底部稍下方开始，确保初始状态完全隐藏
    
    // 底部则根据外层容器加上滚动视差距离，确保不管怎么向上滚动底部都不会悬空出错
    // 再随意往下增加一层随机延长量，使底部保持参差不齐的真实感（虽然看不见）
    const bottomY = containerHeight + speed + 200 + rnd() * vh * 1.5; 

    const joints: BambooJoint[] = [];
    let currentY = startY;
    
    while (currentY < bottomY) {
      const depth = (currentY - startY) / (bottomY - startY);
      const t = Math.pow(depth, 0.4); 
      let w = baseWidth * Math.max(0.01, t);
      if (currentY === startY) w = 0; 
      
      joints.push({ y: currentY, width: w });
      
      const spacing = 40 + rnd() * 40 + depth * 150; 
      currentY += spacing;
    }
    
    const leftSide = joints.map(j => `${x - j.width/2},${j.y}`).join(' L ');
    const rightSide = joints.slice().reverse().map(j => `${x + j.width/2},${j.y}`).join(' L ');
    const trunkPath = `M ${leftSide} L ${rightSide} Z`;
    
    const branches = [];
    
    for (let jIdx = 0; jIdx < joints.length; jIdx++) {
      const joint = joints[jIdx]!;
      const depth = (joint.y - startY) / (bottomY - startY); 
      
      const rawProb = 1 - depth * 1.5; 
      const branchProb = Math.min(0.65, rawProb);
      
      if (branchProb > 0 && rnd() < branchProb) {
        const branchCount = 1 + Math.floor(rnd() * (2 * branchProb));
        
        for (let b = 0; b < branchCount; b++) {
          const side = rnd() > 0.5 ? 1 : -1;
          const angle = side * (20 + rnd() * 50); 
          
          const lengthBase = 30 + (1 - depth) * 110; 
          const branchLength = lengthBase + rnd() * 60; 
          
          const branchThick = 1 + ((1 - depth) * 4) + rnd() * 1;
          
          const rad = angle * Math.PI / 180;
          const startX = x + (side * joint.width / 2);
          const endX = startX + Math.sin(rad) * branchLength;
          const endY = joint.y - Math.cos(rad) * branchLength; 
          
          const leaves = [];
          for (let k = 0; k < 5; k++) { 
            const progress = rnd();
            const leafX = startX + Math.sin(rad) * branchLength * progress;
            const leafY = joint.y - Math.cos(rad) * branchLength * progress;
            
            const leafSide = rnd() > 0.5 ? 1 : -1;
            const rotate = angle + leafSide * (20 + rnd() * 40) - 90;
            const scale = 0.5 + rnd() * 0.8;
            
            leaves.push({
              transform: `translate(${leafX}, ${leafY}) rotate(${rotate}) scale(${scale})`
            });
          }
          
          branches.push({ 
            startX, 
            y: joint.y, 
            endX, 
            endY, 
            width: branchThick,
            leaves 
          });
        }
      }
    }
    
    for (let topB = 0; topB < 2 + rnd() * 3; topB++) {
      const side = rnd() > 0.5 ? 1 : -1;
      const angle = side * (10 + rnd() * 60); 
      const topBranchLength = 120 + rnd() * 100;
      const branchThick = 3 + rnd() * 2; 
      const rad = angle * Math.PI / 180;
      const startX = x;
      const endX = startX + Math.sin(rad) * topBranchLength;
      const endY = startY - Math.cos(rad) * topBranchLength;
      
      const leaves = [];
      for (let k = 0; k < 6; k++) {
        const progress = rnd();
        const leafX = startX + Math.sin(rad) * topBranchLength * progress;
        const leafY = startY - Math.cos(rad) * topBranchLength * progress;
        const leafSide = rnd() > 0.5 ? 1 : -1;
        const rotate = angle + leafSide * (20 + rnd() * 40) - 90;
        const scale = 0.6 + rnd() * 0.7;
        leaves.push({
          transform: `translate(${leafX}, ${leafY}) rotate(${rotate}) scale(${scale})`
        });
      }
      
      branches.push({
        startX, y: startY, endX, endY, width: branchThick, leaves
      });
    }

    generated.push({
      id: i,
      x,
      speed,
      opacity: 0.3 + (zIndex / 10) * 0.6,
      zIndex,
      trunkPath,
      joints,
      branches
    });
  }
  bamboos.value = generated;
}

onMounted(() => {
  setTimeout(() => {
    generateForest();
  }, 10);
  
  if (forestRef.value) {
    resizeObserver = new ResizeObserver(() => {
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(generateForest, 200);
    });
    resizeObserver.observe(forestRef.value);
  }
});

onBeforeUnmount(() => {
  if (resizeObserver && forestRef.value) {
    resizeObserver.unobserve(forestRef.value);
    resizeObserver.disconnect();
  }
  if (debounceTimer) clearTimeout(debounceTimer);
});
</script>

<style scoped>
.bamboo-forest {
  position: absolute;
  top: -55vh;
  left: 0;
  width: 100vw;
  height: calc(100% + 55vh);
  pointer-events: none;
  z-index: 0;
  overflow: visible;
}

.bamboo-svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.bamboo-group {
  transform-origin: center center;
  animation: parallaxScroll linear;
  animation-timeline: scroll();
}

@keyframes parallaxScroll {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(calc(var(--parallax-dist) * -1));
  }
}
</style>
