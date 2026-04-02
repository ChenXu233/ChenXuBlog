<template>
  <canvas id="blossom-canvas" ref="canvasRef"></canvas>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";

const canvasRef = ref<HTMLCanvasElement | null>(null);
let blossomAnimId: number;

let mouseX = 0;
let mouseY = 0;

const handleMouseMove = (e: MouseEvent) => {
  mouseX = e.clientX;
  mouseY = e.clientY + window.scrollY; // global Y
};

const initBlossomCanvas = () => {
  const canvas = canvasRef.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  window.addEventListener("resize", resize);
  resize();

  class Petal {
    x: number;
    y: number;
    size: number;
    speedX: number;
    speedY: number;
    opacity: number;
    angle: number;
    spin: number;

    constructor() {
      this.x = Math.random() * canvas!.width;
      this.y = Math.random() * canvas!.height - canvas!.height;
      this.size = Math.random() * 4 + 3;
      this.speedX = Math.random() * 1 - 0.5;
      this.speedY = Math.random() * 1.5 + 0.8;
      this.opacity = Math.random() * 0.5 + 0.2;
      this.angle = Math.random() * 360;
      this.spin = (Math.random() - 0.5) * 0.1;
    }

    update() {
      this.y += this.speedY;
      this.x += this.speedX + Math.sin(this.angle) * 0.5;
      this.angle += this.spin;

      // Magnetic disruption from mouse
      const dx = this.x - mouseX;
      const dy = this.y - (mouseY - window.scrollY);
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 150) {
        const force = (150 - dist) / 150;
        this.x += dx * force * 0.05;
        this.y += dy * force * 0.02;
        this.angle += force * 0.15;
      }

      if (this.y > canvas!.height) {
        this.y = -10;
        this.x = Math.random() * canvas!.width;
      }
    }

    draw() {
      if (!ctx) return;
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.angle);

      const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, this.size * 2);
      grad.addColorStop(0, `rgba(255, 255, 255, ${this.opacity})`);
      grad.addColorStop(1, `rgba(255, 122, 162, ${this.opacity})`);

      ctx.fillStyle = grad;
      ctx.shadowBlur = 10;
      ctx.shadowColor = `rgba(255, 122, 162, ${this.opacity * 0.5})`;

      ctx.beginPath();
      ctx.moveTo(0, -this.size * 1.5);
      ctx.bezierCurveTo(
        this.size * 1.5,
        -this.size * 1.5,
        this.size * 1.5,
        this.size,
        0,
        this.size * 1.5,
      );
      ctx.bezierCurveTo(
        -this.size * 1.5,
        this.size,
        -this.size * 1.5,
        -this.size * 1.5,
        0,
        -this.size * 1.5,
      );
      ctx.fill();

      ctx.restore();
    }
  }

  const petals = Array.from({ length: 60 }, () => new Petal()); // 减少粒子数优化性能

  const animate = () => {
    blossomAnimId = requestAnimationFrame(animate);

    // 如果已经完全透明不可见，跳过此帧的计算和渲染 (极大节省 GPU 和 CPU)
    if (canvas.style.opacity === "0") return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    petals.forEach((petal) => {
      petal.update();
      petal.draw();
    });
  };
  animate();
};

onMounted(() => {
  window.addEventListener("mousemove", handleMouseMove);
  initBlossomCanvas();
});

onBeforeUnmount(() => {
  window.removeEventListener("mousemove", handleMouseMove);
  cancelAnimationFrame(blossomAnimId);
});
</script>

<style scoped>
#blossom-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}
</style>
