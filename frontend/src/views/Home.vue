<template>
  <div class="home">
    <div class="home-content">
      <div class="home-cards-container">
        <div class="home-card-big" ref="bigCardRefs">
          <h1>欢迎来到ChenXuBlog</h1>
        </div>
      </div>
      <div class="home-cards-container-seconde">
        <div class="home-card" :ref="setSmallCardRef">
          <h2>ChenXuBlog</h2>
        </div>
        <div class="home-card" :ref="setSmallCardRef">
          <h2>ChenXuBlog</h2>
        </div>
        <div class="home-card" :ref="setSmallCardRef">
          <h2>ChenXuBlog</h2>
        </div>
      </div>
      <div class="home-lived-2d-container"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  onMounted,
  onBeforeUnmount,
  ref,
  type ComponentPublicInstance,
} from "vue";

const bigCardRefs = ref<HTMLDivElement | null>(null);
const smallCardRefs = ref<Array<HTMLDivElement | null>>([]);

const setSmallCardRef = (el: Element | ComponentPublicInstance | null) => {
  if (el && (el as HTMLDivElement)) {
    smallCardRefs.value.push(el as HTMLDivElement);
  }
};
onMounted(() => {
  const handleMouseMove = (event: MouseEvent) => {
    const centerX = window.innerWidth / 2;
    const mouseX = event.clientX;
    const maxRotate = 1;
    const rotateY = ((mouseX - centerX) / centerX) * maxRotate;

    if (bigCardRefs.value) {
      bigCardRefs.value.style.setProperty("--rotate-y", `${rotateY + 15}deg`);
    }

    smallCardRefs.value.forEach((card) => {
      if (card) {
        card.style.setProperty("--rotate-y", `${rotateY - 15}deg`);
      }
    });
  };

  window.addEventListener("mousemove", handleMouseMove);

  onBeforeUnmount(() => {
    window.removeEventListener("mousemove", handleMouseMove);
  });
});
</script>

<style scoped>
.home {
  background-color: #f5f5f5;
  background-image: url("/yunxi.jpg");
  background-size: cover;
  background-position: 20% center;
  background-repeat: no-repeat;
  min-height: 100vh;
  z-index: 0;
  transition: all 0.5s ease-in-out;
}

.home-content {
  position: relative;
}

.home-cards-container {
  position: absolute;
  top: 20vh;
  left: 10vw;
  perspective: 70vh;
  transition: all 0.5s ease-in-out;
}

.home-cards-container-seconde {
  position: absolute;
  top: 35vh;
  left: 30vw;
  perspective: 70vh;
  transition: all 0.5s ease-in-out;
}

.home-card-big,
.home-card {
  width: 25vw;
  height: 13vh;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 1vh;
  padding: 20px;
  margin: 20px;
}

.home-card:not(.home-card-big) {
  animation: rotateFloatSmallCard 4s ease-in-out infinite;
}

.home-card-big {
  width: 30vw;
  height: 60vh;
  animation: rotateFloatBigCard 6s ease-in-out infinite;
}

@keyframes rotateFloatBigCard {
  0% {
    transform: translateY(0) rotateY(var(--rotate-y, 15deg));
  }
  50% {
    transform: translateY(-20px) rotateY(var(--rotate-y, 15deg));
  }
  100% {
    transform: translateY(0) rotateY(var(--rotate-y, 15deg));
  }
}

@keyframes rotateFloatSmallCard {
  0% {
    transform: translateY(0) rotateY(var(--rotate-y, -15deg));
  }
  50% {
    transform: translateY(-20px) rotateY(var(--rotate-y, -15deg));
  }
  100% {
    transform: translateY(0) rotateY(var(--rotate-y, -15deg));
  }
}

@media (max-width: 1200px) {
  .home {
    background-image: url("/yunxi.jpg");
    background-position: center top;
  }
  .home-cards-container {
    top: 20vh;
    left: 10vw;
  }
  .home-cards-container-seconde {
    top: 35vh;
    left: 35vw;
  }
  .home-card-big,
  .home-card {
    width: 30vw;
    height: 13vh;
  }
  .home-card-big {
    width: 35vw;
    height: 60vh;
  }
}

@media (max-width: 480px) {
  .home-lived-2d-container {
    display: none;
  }
}
</style>
