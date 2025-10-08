<template>
  <div class="home">
    <div class="home-content">
      <div class="home-cards-container" ref="bigCardRefs">
        <div class="home-card-big-container">
          <div class="home-card-big-tips-card">
            <h1>欢迎来到ChenXuBlog</h1>
          </div>
          <router-link to="/blog">
            <div class="home-card-big card-big">
              <h2>博客</h2>
            </div>
          </router-link>
        </div>
      </div>
      <div class="home-cards-container-seconde" ref="smallCardRefs">
        <router-link to="/archive">
          <div class="home-card card-1">
            <h2>归档</h2>
          </div>
        </router-link>
        <router-link to="/friend">
          <div class="home-card card-2">
            <h2>友链</h2>
          </div>
        </router-link>
        <router-link to="/diary">
          <div class="home-card card-3">
            <h2>随谈</h2>
          </div>
        </router-link>
      </div>
      <div class="home-lived-2d-container"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from "vue";

const bigCardRefs = ref<HTMLDivElement | null>(null);
const smallCardRefs = ref<HTMLDivElement | null>(null);

onMounted(() => {
  const handleMouseMove = (event: MouseEvent) => {
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    const maxRotate = 3;
    const rotateY = ((mouseX - centerX) / centerX) * maxRotate;
    const rotateX = ((mouseY - centerY) / centerY) * maxRotate;

    if (bigCardRefs.value) {
      bigCardRefs.value.style.setProperty("--rotate-y", `${rotateY + 15}deg`);
      bigCardRefs.value.style.setProperty("--rotate-x", `${-rotateX + 2}deg`);
    }

    if (smallCardRefs.value) {
      smallCardRefs.value.style.setProperty("--rotate-y", `${rotateY - 15}deg`);
      smallCardRefs.value.style.setProperty("--rotate-x", `${-rotateX + 2}deg`);
    }
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
  perspective: 100vh;
  perspective-origin: 50% 0%;
}

.home-cards-container {
  position: absolute;
  top: 20vh;
  left: 10vw;
  transition: all 0.5s ease-in-out;
  animation: rotateFloatBigCard 6s ease-in-out infinite;
}

.home-cards-container-seconde {
  position: absolute;
  top: 35vh;
  left: 35vw;
  transition: all 0.5s ease-in-out;
  animation: rotateFloatSmallCard 4s ease-in-out infinite;
}

.home-card-big-container {
  transition: all 0.5s ease-in-out;
}

.home-card-big,
.home-card {
  width: 25vw;
  height: 13vh;
  border-radius: 1vh;
  padding: 3vh;
  margin: 3vh;
}

.home-card-big {
  width: 50vh;
  height: 50vh;
}

.home-card-big-tips-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 1vh;
  padding: 1vh;
  margin: 3vh;
}

.home-card-big-tips-card h1 {
  font-size: 2.5vh;
  padding: 0vh 2vh;
  color: blue;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.card-1,
.card-2,
.card-3,
.card-big,
.home-card-big-tips-card {
  transition: transform 0.3s ease;
}

.card-1 {
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  color: white;
}

.card-2 {
  background: linear-gradient(135deg, #ff6a00, #ee0979);
  box-shadow: 0 4px 15px rgba(255, 106, 0, 0.3);
  color: white;
}

.card-3 {
  background: linear-gradient(135deg, #00dbde, #fc00ff);
}

.card-big {
  background: linear-gradient(135deg, #ff512f, #dd2476);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.3);
}

.card-1:hover,
.card-2:hover,
.card-3:hover,
.card-big:hover,
.home-card-big-tips-card:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
  transform: scale(1.05);
}

@keyframes rotateFloatBigCard {
  0% {
    transform: translateY(0) rotateY(var(--rotate-y, 15deg))
      rotateX(var(--rotate-x, 0deg));
  }
  50% {
    transform: translateY(-20px) rotateY(var(--rotate-y, 15deg))
      rotateX(var(--rotate-x, 0deg));
  }
  100% {
    transform: translateY(0) rotateY(var(--rotate-y, 15deg))
      rotateX(var(--rotate-x, 0deg));
  }
}

@keyframes rotateFloatSmallCard {
  0% {
    transform: translateY(0) rotateY(var(--rotate-y, -15deg))
      rotateX(var(--rotate-x, 0deg));
  }
  50% {
    transform: translateY(-20px) rotateY(var(--rotate-y, -15deg))
      rotateX(var(--rotate-x, 0deg));
  }
  100% {
    transform: translateY(0) rotateY(var(--rotate-y, -15deg))
      rotateX(var(--rotate-x, 0deg));
  }
}

@media (max-width: 1200px) {
  .home {
    background-image: url("/yunxi.jpg");
    background-position: center top;
  }
  .home-cards-container {
    top: 15vh;
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
