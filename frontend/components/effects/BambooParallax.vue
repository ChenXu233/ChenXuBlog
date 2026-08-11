<template>
  <div class="bamboo-forest" ref="forestRef">
    <svg
      class="bamboo-svg"
      preserveAspectRatio="none"
      xmlns="http://www.w3.org/2000/svg"
    >
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
        :style="{
          '--parallax-dist': bamboo.speed + 'px',
          opacity: bamboo.opacity,
        }"
      >
        <!-- 主干 -->
        <path :d="bamboo.trunkPath" fill="url(#stalkGrad)" />

        <!-- 竹壳/竹节 -->
        <rect
          v-for="(j, idx) in bamboo.joints"
          :key="'j' + idx"
          :x="j.x - j.width / 2 - 2"
          :y="j.y"
          :width="j.width + 4"
          height="4"
          fill="#7a9073"
          rx="2"
        />

        <!-- 分枝结构 -->
        <line
          v-for="(seg, sIdx) in bamboo.branchSegments"
          :key="'s' + sIdx"
          :x1="seg.x1"
          :y1="seg.y1"
          :x2="seg.x2"
          :y2="seg.y2"
          stroke="#9fc4a6"
          :stroke-width="seg.width"
          stroke-linecap="round"
        />

        <!-- 叶子 -->
        <g
          v-for="(leaf, lKey) in bamboo.leaves"
          :key="'l' + lKey"
          :transform="leaf.transform"
          :opacity="leaf.opacity"
        >
          <path d="M 0,0 Q 20,-10 40,0 Q 20,10 0,0 Z" fill="url(#leafGrad)" />
        </g>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";

defineProps<{ progress?: number }>();
const forestRef = ref<HTMLElement | null>(null);

function seed(s: number) {
  return function () {
    s = Math.sin(s) * 10000;
    return s - Math.floor(s);
  };
}

interface BambooJoint {
  x: number;
  y: number;
  width: number;
}

interface BambooBranchSegment {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  width: number;
}

interface BambooLeaf {
  transform: string;
  opacity: number;
}

interface Bamboo {
  id: number;
  x: number;
  speed: number;
  opacity: number;
  zIndex: number;
  trunkPath: string;
  joints: BambooJoint[];
  branchSegments: BambooBranchSegment[];
  leaves: BambooLeaf[];
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

  const bambooCount = Math.max(5, Math.floor(vw / 300));

  for (let i = 0; i < bambooCount; i++) {
    const rnd = seed(191981 + i);
    const x = -vw * 0.1 + rnd() * (vw * 1.2);
    const zIndex = Math.floor(rnd() * 10);
    const baseWidth = 15 + zIndex * 2.5 + rnd() * 20;

    const speed = 200 + zIndex * 400;

    const startY = 0.8 * vh;
    const bottomY = containerHeight + speed + 200 + rnd() * vh * 1.5;

    // 主干重量向一边倾斜
    const leanDirection = rnd() > 0.5 ? 1 : -1;
    const maxLean = 100 + rnd() * 200; // 顶部最大偏移量

    const joints: BambooJoint[] = [];
    let currentY = startY;

    while (currentY < bottomY) {
      const depth = (currentY - startY) / (bottomY - startY); // 从顶到底: 0 -> 1

      // 计算这一节的 x 坐标（越往上偏移越大，抛物线弯曲）
      const leanFactor = Math.pow(1 - depth, 2);
      const currentX = x + leanDirection * maxLean * leanFactor;

      const t = Math.pow(depth, 0.4);
      let w = baseWidth * Math.max(0.01, t);
      if (currentY === startY) w = 0;

      joints.push({ x: currentX, y: currentY, width: w });

      const spacing = 40 + rnd() * 40 + depth * 150;
      currentY += spacing;
    }

    const leftSide = joints
      .map((j) => `${j.x - j.width / 2},${j.y}`)
      .join(" L ");
    const rightSide = joints
      .slice()
      .reverse()
      .map((j) => `${j.x + j.width / 2},${j.y}`)
      .join(" L ");
    const trunkPath = `M ${leftSide} L ${rightSide} Z`;

    const branchSegments: BambooBranchSegment[] = [];
    const leaves: BambooLeaf[] = [];

    function addLeafCluster(
      lx: number,
      ly: number,
      branchAngleDeg: number,
      branchDepth: number,
    ) {
      const leafCount = 1 + Math.floor(rnd() * 3); // 减少叶子数量
      for (let k = 0; k < leafCount; k++) {
        // 根据所在分支的角度区分左右侧
        const sideSign = branchAngleDeg >= 0 ? 1 : -1;
        // 叶子的角度强制设定在 60~90 度（外放自然下垂或平展）
        const leafDeg = sideSign * (90 + rnd() * 60);

        const svgRot = leafDeg - 90;
        // 叶子画大一点
        const scale = 1.2 + rnd() * 0.8;
        const ox = (rnd() - 0.5) * 6;
        const oy = (rnd() - 0.5) * 6;

        // 越顶端的叶子透明度越低（向深处过渡逐渐变透明，顶部不透明）
        const leafOpacity = 0.3 + (1 - branchDepth) * 0.7 + (rnd() * 0.2 - 0.1);

        leaves.push({
          transform: `translate(${lx + ox}, ${
            ly + oy
          }) rotate(${svgRot}) scale(${scale})`,
          opacity: Math.max(1, Math.max(0.1, leafOpacity)),
        });
      }
    }

    function buildBranchTree(
      bx: number,
      by: number,
      angleDeg: number,
      length: number,
      width: number,
      level: number,
      branchDepth: number,
    ) {
      if (level > 3) return;

      let numSegments = 0;
      if (level === 1) numSegments = 4 + Math.floor(rnd() * 2);
      // 一级枝条分节变多（像主干一样有节）
      else if (level === 2) numSegments = 2 + Math.floor(rnd() * 2);
      else numSegments = 1; // 三级分支只有1段非常短

      let cx = bx;
      let cy = by;
      let curAngle = angleDeg;

      const parentJointsX: number[] = [];
      const parentJointsY: number[] = [];
      const parentJointsW: number[] = [];

      const segLen = length / numSegments;

      for (let s = 0; s < numSegments; s++) {
        const t = s / numSegments;
        const curWidth = Math.max(0.5, width * (1 - t * 0.6));

        // 角度变化：一级枝条尽量挺直（角度微小偏移），其余有一定弯曲
        if (level === 1) {
          curAngle += (rnd() - 0.5) * 5;
        } else {
          curAngle += (rnd() - 0.5) * 15;
        }

        const rad = ((curAngle - 90) * Math.PI) / 180;
        const nx = cx + Math.cos(rad) * segLen;
        const ny = cy + Math.sin(rad) * segLen;

        branchSegments.push({
          x1: cx,
          y1: cy,
          x2: nx,
          y2: ny,
          width: curWidth,
        });

        parentJointsX.push(nx);
        parentJointsY.push(ny);
        parentJointsW.push(curWidth);

        cx = nx;
        cy = ny;
      }

      // 三级分支末端一定要有竹叶（二级分支作为末梢也挂载叶子）
      if (level === 3 || level === 2) {
        addLeafCluster(cx, cy, curAngle, branchDepth);
      }

      for (let s = 1; s < numSegments; s++) {
        if (level === 1) {
          const symProb = 1 - branchDepth * 2.5;
          // 级数越深枝节越短
          const childLen = length * 0.3 + rnd() * 15;
          const childWidth = Math.max(0.5, (parentJointsW[s] ?? 1) * 0.5);

          if (rnd() < symProb) {
            // 对称的二级分支
            const angle1 = curAngle + 30 + rnd() * 20;
            const angle2 = curAngle - 30 - rnd() * 20;
            buildBranchTree(
              parentJointsX[s]!,
              parentJointsY[s]!,
              angle1,
              childLen,
              childWidth,
              2,
              branchDepth,
            );
            buildBranchTree(
              parentJointsX[s]!,
              parentJointsY[s]!,
              angle2,
              childLen,
              childWidth,
              2,
              branchDepth,
            );
          } else {
            // 单侧不对称的二级分支
            const side = rnd() > 0.5 ? 1 : -1;
            const childAngle = curAngle + side * (30 + rnd() * 20);
            buildBranchTree(
              parentJointsX[s]!,
              parentJointsY[s]!,
              childAngle,
              childLen,
              childWidth,
              2,
              branchDepth,
            );
          }
        } else if (level === 2) {
          // 二级分支有概率直接变成3级分支
          if (rnd() < 0.7) {
            const symProb = 0.5 * (1 - branchDepth * 2.5);
            // 三级枝极其短（末梢）
            const childLen = 10 + rnd() * 10;
            const childWidth = Math.max(0.5, (parentJointsW[s] ?? 1) * 0.6);
            if (rnd() < symProb) {
              const angle1 = curAngle + 20 + rnd() * 20;
              const angle2 = curAngle - 20 - rnd() * 20;
              buildBranchTree(
                parentJointsX[s]!,
                parentJointsY[s]!,
                angle1,
                childLen,
                childWidth,
                3,
                branchDepth,
              );
              buildBranchTree(
                parentJointsX[s]!,
                parentJointsY[s]!,
                angle2,
                childLen,
                childWidth,
                3,
                branchDepth,
              );
            } else {
              const side = rnd() > 0.5 ? 1 : -1;
              const childAngle = curAngle + side * (20 + rnd() * 20);
              buildBranchTree(
                parentJointsX[s]!,
                parentJointsY[s]!,
                childAngle,
                childLen,
                childWidth,
                3,
                branchDepth,
              );
            }
          }
        }
      }
    }

    const numJoints = joints.length;
    const maxBranchJoints = 13 + Math.floor(rnd() * 5); // 顶部大约13~17节有分支
    for (let jIdx = 1; jIdx < numJoints; jIdx++) {
      const joint = joints[jIdx];
      if (!joint) continue;
      const depth = (joint.y - startY) / (bottomY - startY);

      if (jIdx <= maxBranchJoints) {
        // 主干长出一级分支，越到顶端，越容易对称
        const symProbRoot = 1 - depth * 2.5;
        const startSides =
          rnd() < symProbRoot ? [1, -1] : [rnd() > 0.5 ? 1 : -1];

        for (const side of startSides) {
          const angleDeg = 30 + rnd() * 20;
          // 为了迎合弯曲的主干，整体角度向弯曲一侧偏转
          const baseBranchAngle =
            side * angleDeg + leanDirection * 20 * Math.pow(1 - depth, 2);

          // 越到顶端一代分支越长，甚至比三节竹子长（通过深度反比增加基础长度）
          const maxL = 150 + (1 - depth) * 200 + rnd() * 50;
          const branchBaseWidth = Math.max(
            1.5,
            joint.width * (0.3 + rnd() * 0.2),
          );

          buildBranchTree(
            joint.x + side * (joint.width / 2),
            joint.y,
            baseBranchAngle,
            maxL,
            branchBaseWidth,
            1,
            depth,
          );
        }
      }
    }

    for (let topB = 0; topB < 2 + rnd() * 2; topB++) {
      const side = rnd() > 0.5 ? 1 : -1;
      const angle = side * (10 + rnd() * 20) + leanDirection * 30;
      const topBranchLength = 120 + rnd() * 60;
      const branchBaseWidth = Math.max(1.5, baseWidth * 0.15);
      const topJoint = joints[0];
      if (!topJoint) continue;

      buildBranchTree(
        topJoint.x,
        startY,
        angle,
        topBranchLength,
        branchBaseWidth,
        1,
        0,
      ); // 顶端深度强制为 0
    }

    generated.push({
      id: i,
      x,
      speed,
      opacity: 0.6 + (zIndex / 10) * 0.4,
      zIndex,
      trunkPath,
      joints,
      branchSegments,
      leaves,
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
