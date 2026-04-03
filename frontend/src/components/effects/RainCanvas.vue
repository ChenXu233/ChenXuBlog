<template>
  <div class="rain-container">
    <canvas id="rain-canvas" ref="rainCanvasRef"></canvas>
    <audio
      :ref="
        (el) => {
          if (el) thunderAudioRefs.push(el as HTMLAudioElement);
        }
      "
      src="https://assets.mixkit.co/active_storage/sfx/2391/2391-preview.mp3"
      preload="auto"
      loop
    ></audio>
    <audio
      :ref="
        (el) => {
          if (el) thunderAudioRefs.push(el as HTMLAudioElement);
        }
      "
      src="https://assets.mixkit.co/active_storage/sfx/2391/2391-preview.mp3"
      preload="auto"
      loop
    ></audio>
    <div class="thunder-overlay" :class="{ 'is-flashing': isFlashing }"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";

const rainCanvasRef = ref<HTMLCanvasElement | null>(null);
let rainAnimId: number;

const thunderAudioRefs: HTMLAudioElement[] = [];
const isFlashing = ref(false);
let fadeInterval: number | null = null;
let hasPlayedThunder = false;
let thunderObserver: IntersectionObserver | null = null;
let thunderFlashInterval: number | null = null;
let hScrollObserver: IntersectionObserver | null = null;

const triggerFlash = () => {
  isFlashing.value = true;
  document.body.classList.add("is-flashing");
  setTimeout(() => {
    isFlashing.value = false;
    document.body.classList.remove("is-flashing");
  }, 100);
  setTimeout(() => {
    isFlashing.value = true;
    document.body.classList.add("is-flashing");
    setTimeout(() => {
      isFlashing.value = false;
      document.body.classList.remove("is-flashing");
    }, 150);
  }, 200);
};

const fadeOutAudio = () => {
  thunderAudioRefs.forEach((audio) => {
    if (audio.paused) return;
    if (fadeInterval) clearInterval(fadeInterval);
    fadeInterval = window.setInterval(() => {
      const currentVol = audio.volume;
      if (currentVol > 0.05) {
        audio.volume = currentVol - 0.05;
      } else {
        audio.pause();
        audio.volume = 0.5;
        clearInterval(fadeInterval!);
      }
    }, 100);
  });
  if (thunderFlashInterval) clearInterval(thunderFlashInterval);
};

const isCanvasVisible = () => {
  const canvas = rainCanvasRef.value;
  return canvas && canvas.style.opacity !== "0";
};

const playThunder = (audio: HTMLAudioElement, delay: number = 0) => {
  if (!isCanvasVisible()) return;
  if (delay > 0) {
    setTimeout(() => {
      if (!isCanvasVisible()) return;
      audio.currentTime = 0;
      audio.volume = 0.5;
      audio
        .play()
        .then(() => triggerFlash())
        .catch(() => {});
    }, delay);
  } else {
    audio.currentTime = 0;
    audio.volume = 0.5;
    audio
      .play()
      .then(() => triggerFlash())
      .catch(() => {});
  }
};

const fadeInAudio = () => {
  if (!isCanvasVisible()) return;
  if (fadeInterval) clearInterval(fadeInterval);
  if (thunderFlashInterval) clearInterval(thunderFlashInterval);

  const audios = thunderAudioRefs;
  // Randomly decide 1 or 2 audio tracks (1 with higher probability)
  const trackCount = Math.random() < 0.6 ? 1 : 2;

  if (!hasPlayedThunder) {
    hasPlayedThunder = true;
    // First time: always play 1 track immediately for flash sync
    playThunder(audios[0]);
  } else {
    // Subsequent plays: randomly play 1 or 2 tracks
    if (trackCount === 1) {
      playThunder(audios[0]);
    } else {
      // Stagger two tracks with longer delay for natural thunder echo
      playThunder(audios[0]);
      playThunder(audios[1], 2000 + Math.random() * 4000);
    }
  }

  // Schedule next thunder after a random interval (5-12 seconds)
  const scheduleNextThunder = () => {
    thunderFlashInterval = window.setTimeout(
      () => {
        const count = Math.random() < 0.6 ? 1 : 2;
        if (count === 1) {
          playThunder(audios[Math.floor(Math.random() * audios.length)]);
        } else {
          const idx1 = Math.floor(Math.random() * audios.length);
          let idx2 = Math.floor(Math.random() * audios.length);
          while (idx2 === idx1)
            idx2 = Math.floor(Math.random() * audios.length);
          playThunder(audios[idx1]);
          playThunder(audios[idx2], 2000 + Math.random() * 4000);
        }
        scheduleNextThunder();
      },
      5000 + Math.random() * 7000,
    );
  };
  scheduleNextThunder();
};

const initRainCanvas = () => {
  const canvas = rainCanvasRef.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  window.addEventListener("resize", resize);

  // Give it a tiny delay to ensure proper DOM calculation
  setTimeout(resize, 50);

  class Ripple {
    x: number;
    y: number;
    radius: number;
    maxRadius: number;
    speed: number;
    opacity: number;
    z: number;
    active: boolean;

    constructor(x: number, y: number, z: number) {
      this.x = x;
      this.y = y;
      this.z = z;
      this.radius = 0;
      this.maxRadius = (Math.random() * 15 + 10) * z;
      this.speed = (Math.random() * 0.5 + 0.5) * z;
      this.opacity = z * 0.5 + 0.5;
      this.active = true;
    }

    update() {
      if (!this.active) return;
      this.radius += this.speed;
      this.opacity -= 0.01;
      if (this.radius > this.maxRadius || this.opacity <= 0) {
        this.active = false;
      }
    }

    draw() {
      if (!this.active || !ctx) return;
      ctx.beginPath();
      ctx.ellipse(
        this.x,
        this.y,
        this.radius,
        this.radius * 0.3,
        0,
        0,
        Math.PI * 2,
      );
      ctx.shadowBlur = 10;
      ctx.shadowColor = `rgba(200, 240, 255, ${Math.max(0, this.opacity)})`;
      ctx.strokeStyle = `rgba(255, 255, 255, ${this.opacity})`;
      ctx.lineWidth = 1.5 * this.z;
      ctx.stroke();
    }
  }

  class RainDrop {
    x: number;
    y: number;
    z: number;
    length: number;
    speedY: number;
    opacity: number;
    thickness: number;

    constructor() {
      this.x = Math.random() * canvas!.width;
      this.y = Math.random() * canvas!.height;
      this.z = Math.random() * 0.8 + 0.2; // 0.2 to 1 for depth
      this.length = (Math.random() * 60 + 30) * this.z;
      this.speedY = (Math.random() * 6 + 4) * this.z + 2;
      this.opacity = this.z * 0.5 + 0.5;
      this.thickness = this.z * 1.5 + 0.5;
    }

    update() {
      this.y += this.speedY;
      if (this.y > canvas!.height) {
        ripples.push(new Ripple(this.x, canvas!.height, this.z));
        this.y = -this.length;
        this.x = Math.random() * canvas!.width;
        this.z = Math.random() * 0.8 + 0.2;
        this.length = (Math.random() * 60 + 30) * this.z;
        this.speedY = (Math.random() * 6 + 4) * this.z + 2;
        this.opacity = this.z * 0.5 + 0.5;
        this.thickness = this.z * 1.5 + 0.5;
      }
    }

    draw() {
      if (!ctx) return;
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(this.x, this.y + this.length);
      ctx.shadowBlur = 5;
      ctx.shadowColor = `rgba(180, 230, 255, ${this.opacity})`;
      ctx.strokeStyle = `rgba(255, 255, 255, ${this.opacity})`;
      ctx.lineWidth = this.thickness;
      ctx.stroke();
    }
  }

  const drops = Array.from({ length: 80 }, () => new RainDrop()); // 减少粒子数优化性能
  let ripples: Ripple[] = [];

  const animate = () => {
    rainAnimId = requestAnimationFrame(animate);

    // 如果已经完全透明不可见，跳过此帧的计算和渲染 (极大节省 GPU 和 CPU)
    if (canvas!.style.opacity === "0") return;

    ctx.clearRect(0, 0, canvas!.width, canvas!.height);
    ctx.shadowBlur = 0;
    ctx.lineCap = "round";

    drops.forEach((drop) => {
      drop.update();
      drop.draw();
    });

    ripples.forEach((rip) => {
      rip.update();
      rip.draw();
    });
    ripples = ripples.filter((rip) => rip.active);
  };
  animate();
};

onMounted(() => {
  // Initialize rain after layout stabilizes
  setTimeout(() => {
    initRainCanvas();
  }, 300);

  setTimeout(() => {
    const introSection = document.querySelector(".intro-section");
    if (introSection) {
      thunderObserver = new IntersectionObserver(
        (entries) => {
          const entry = entries[0];
          if (entry) {
            if (entry.isIntersecting) {
              fadeInAudio();
            } else {
              fadeOutAudio();
            }
          }
        },
        { threshold: 0.3 },
      );
      thunderObserver.observe(introSection);

      window.addEventListener(
        "click",
        () => {
          if (!hasPlayedThunder) {
            const rect = introSection.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
              thunderAudioRef.value?.play().catch(() => {});
              hasPlayedThunder = true;
            }
          }
        },
        { once: true },
      );

      // Fade out audio when entering horizontal scroll section
      const hScrollSection = document.querySelector(".h-scroll-wrapper");
      if (hScrollSection) {
        hScrollObserver = new IntersectionObserver(
          (entries) => {
            const entry = entries[0];
            if (entry && entry.isIntersecting) {
              fadeOutAudio();
            }
          },
          { threshold: 0.1 },
        );
        hScrollObserver.observe(hScrollSection);
      }
    }
  }, 500);
});

onBeforeUnmount(() => {
  cancelAnimationFrame(rainAnimId);
  if (thunderObserver) thunderObserver.disconnect();
  if (hScrollObserver) hScrollObserver.disconnect();
  if (thunderFlashInterval) clearInterval(thunderFlashInterval);
});
</script>

<style scoped>
.rain-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.thunder-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.4);
  mix-blend-mode: overlay;
  pointer-events: none;
  opacity: 0;
}

.thunder-overlay.is-flashing {
  animation: flash-overlay 0.3s ease-out forwards;
}

@keyframes flash-overlay {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

#rain-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
