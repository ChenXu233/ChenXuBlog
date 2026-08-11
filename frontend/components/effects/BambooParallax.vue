<template>
  <div class="bamboo-forest" ref="forestRef">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from "vue";

// ponytail: canvas 版渲染 —— 原 SVG 版每根竹子约 500+ DOM 节点（竹节/分枝/叶子），
// 6 根就是 ~3000 节点还各自跑 scroll() 动画，低端机明显卡顿。
// 生成算法（generateForest）完全保留，仅渲染层换成单个 canvas 每帧重绘（1-3ms）。

const props = defineProps<{ progress?: number }>();
const forestRef = ref<HTMLElement | null>(null);
const canvasRef = ref<HTMLCanvasElement | null>(null);

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
  x: number;
  y: number;
  rot: number;
  scale: number;
  opacity: number;
}

interface Bamboo {
  id: number;
  speed: number;
  opacity: number;
  minX: number;
  maxX: number;
  startY: number;
  bottomY: number;
  joints: BambooJoint[];
  branchSegments: BambooBranchSegment[];
  leaves: BambooLeaf[];
}

const bamboos = ref<Bamboo[]>([]);
let resizeObserver: ResizeObserver | null = null;
let debounceTimer: ReturnType<typeof setTimeout> | null = null;
let maxExtra = 0; // 竹子超出容器底部的最大高度（canvas 需要包含它）

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
          x: lx + ox,
          y: ly + oy,
          rot: svgRot,
          scale,
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

    // 主干包围盒（用于 stalk 渐变，等价于 SVG objectBoundingBox）
    let minX = Infinity;
    let maxX = -Infinity;
    for (const j of joints) {
      if (j.x - j.width / 2 < minX) minX = j.x - j.width / 2;
      if (j.x + j.width / 2 > maxX) maxX = j.x + j.width / 2;
    }

    generated.push({
      id: i,
      speed,
      opacity: 0.6 + (zIndex / 10) * 0.4,
      minX,
      maxX,
      startY,
      bottomY,
      joints,
      branchSegments,
      leaves,
    });
  }
  bamboos.value = generated;
  // 竹子底部最大超出容器的高度（原版 SVG overflow:visible 会显示这部分）
  maxExtra = 0;
  for (const b of generated) {
    maxExtra = Math.max(maxExtra, b.bottomY - containerHeight);
  }
}

// ---------- canvas 渲染（离屏分层） ----------
// 竹子内容是静态的，只在生成时画一次到离屏 canvas；
// 滚动视差每帧只做 drawImage 平移（6 次位块传送 ≈ 0.1-1ms），
// 替代 SVG 版每根竹子 500+ DOM 节点 + scroll() 动画。

let ctx: CanvasRenderingContext2D | null = null;
let rafId = 0;
const offscreenMap = new Map<number, HTMLCanvasElement>();

let leafPath: Path2D | null = null;
let leafGrad: CanvasGradient | null = null;

function setupCanvas() {
  const canvas = canvasRef.value;
  const forest = forestRef.value;
  if (!canvas || !forest) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 2); // 背景层，DPR 封顶 2 即可
  const rect = forest.getBoundingClientRect();
  // 高度含竹子底部超出容器的部分（对齐原版 SVG overflow:visible）
  const h = rect.height + maxExtra;
  canvas.width = Math.max(1, Math.round(rect.width * dpr));
  canvas.height = Math.max(1, Math.round(h * dpr));
  canvas.style.width = rect.width + "px";
  canvas.style.height = h + "px";
  ctx = canvas.getContext("2d");
  if (!ctx) return;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

// 每根竹子画到自己的离屏 canvas（生成一次，滚动不再重绘）
function buildOffscreen(b: Bamboo, dpr: number) {
  const c = document.createElement("canvas");
  c.width = Math.max(1, Math.round((b.maxX - b.minX + 60) * dpr));
  c.height = Math.max(1, Math.round(b.bottomY * dpr));
  const g = c.getContext("2d");
  if (!g) return;
  g.setTransform(dpr, 0, 0, dpr, 0, 0);

  // 主干（等价 trunkPath 多边形 + stalkGrad 渐变）
  const grad = g.createLinearGradient(b.minX, b.startY, b.maxX, b.startY);
  grad.addColorStop(0, "#9db495");
  grad.addColorStop(0.4, "#dce5d8");
  grad.addColorStop(0.6, "#dce5d8");
  grad.addColorStop(1, "#8fa486");
  g.fillStyle = grad;
  g.beginPath();
  const j = b.joints;
  g.moveTo(j[0].x - j[0].width / 2, j[0].y);
  for (let i = 1; i < j.length; i++) {
    g.lineTo(j[i].x - j[i].width / 2, j[i].y);
  }
  for (let i = j.length - 1; i >= 0; i--) {
    g.lineTo(j[i].x + j[i].width / 2, j[i].y);
  }
  g.closePath();
  g.fill();

  // 竹节（等价 rect + rx=2）
  g.fillStyle = "#7a9073";
  for (const jt of b.joints) {
    g.roundRect(jt.x - jt.width / 2 - 2, jt.y, jt.width + 4, 4, 2);
    g.fill();
  }

  // 分枝（等价 line + round cap）
  g.strokeStyle = "#9fc4a6";
  g.lineCap = "round";
  for (const seg of b.branchSegments) {
    g.lineWidth = seg.width;
    g.beginPath();
    g.moveTo(seg.x1, seg.y1);
    g.lineTo(seg.x2, seg.y2);
    g.stroke();
  }

  // 叶子（等价 translate/rotate/scale + leafGrad）
  if (leafPath && leafGrad) {
    g.fillStyle = leafGrad;
    for (const leaf of b.leaves) {
      g.save();
      g.globalAlpha = Math.min(1, leaf.opacity);
      g.translate(leaf.x, leaf.y);
      g.rotate((leaf.rot * Math.PI) / 180);
      g.scale(leaf.scale, leaf.scale);
      g.fill(leafPath);
      g.restore();
    }
  }

  offscreenMap.set(b.id, c);
}

function buildAllOffscreen() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  offscreenMap.clear();

  if (!leafPath || !leafGrad) {
    leafPath = new Path2D("M 0,0 Q 20,-10 40,0 Q 20,10 0,0 Z");
    // 所有叶子本地包围盒都是 40x20，渐变共用一份（等价 SVG leafGrad objectBoundingBox）
    const t = document.createElement("canvas").getContext("2d");
    if (t) {
      leafGrad = t.createLinearGradient(0, 0, 40, 0);
      leafGrad.addColorStop(0, "#8fa486");
      leafGrad.addColorStop(1, "#b0c4a8");
    }
  }

  for (const b of bamboos.value) buildOffscreen(b, dpr);
}

function draw() {
  if (!ctx || !canvasRef.value) return;
  const canvas = canvasRef.value;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const progress = props.progress ?? 0;

  for (const b of bamboos.value) {
    const off = offscreenMap.get(b.id);
    if (!off) continue;
    ctx.save();
    ctx.globalAlpha = b.opacity;
    // 视差：竹子随滚动进度整体上移（等价原 CSS translateY(-speed * progress)）
    ctx.drawImage(off, 0, -b.speed * progress);
    ctx.restore();
  }
}

function scheduleDraw() {
  if (rafId) return;
  rafId = requestAnimationFrame(() => {
    rafId = 0;
    draw();
  });
}

watch(
  () => props.progress,
  () => scheduleDraw(),
);

onMounted(() => {
  setTimeout(() => {
    generateForest();
    buildAllOffscreen();
    setupCanvas();
    draw();
  }, 10);

  if (forestRef.value) {
    resizeObserver = new ResizeObserver(() => {
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        generateForest();
        buildAllOffscreen();
        setupCanvas();
        draw();
      }, 200);
    });
    resizeObserver.observe(forestRef.value);
  }
});

onBeforeUnmount(() => {
  if (rafId) cancelAnimationFrame(rafId);
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

.bamboo-forest canvas {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
