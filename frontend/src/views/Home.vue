<template>
  <div class="home">
    <div class="home-content">
      <div class="card-container-left" ref="bigCardRefs">
        <div class="card big-card tips-card">
          <h1>欢迎来到ChenXuBlog</h1>
        </div>
        <div class="home-card-big card-big">
          <el-carousel
              :interval="4000"
              trigger="click"
              height="40vh"
              indicator-position="outside"
              motion-blur="true"
          >
            <router-link to="/blog">
              <el-carousel-item
                  style="
                    background-image: url(/yunxi.jpg);
                    background-size: cover;
                    background-position: center;
                  "
              >
              </el-carousel-item>
            </router-link>
            <el-carousel-item>
              <router-link to="/archive">
                <h2>归档</h2>
              </router-link>
            </el-carousel-item>
            <el-carousel-item>
              <router-link to="/friend">
                <h2>友链</h2>
              </router-link>
            </el-carousel-item>
            <el-carousel-item>
              <router-link to="/diary">
                <h2>随谈</h2>
              </router-link>
            </el-carousel-item>
          </el-carousel>
        </div>
      </div>
      <div class="card-container-right" ref="smallCardRefs">
        <router-link to="/archive">
          <div class="card card-1">
            <h2>归档</h2>
          </div>
        </router-link>
        <router-link to="/friend">
          <div class="card card-2">
            <h2>友链</h2>
          </div>
        </router-link>
        <router-link to="/diary">
          <div class="card card-3">
            <h2>随谈</h2>
          </div>
        </router-link>
      </div>
      <div class="lived2d-container"></div>
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
  perspective-origin: 50% 0;
}

.card-container-left {
  position: absolute;
  top: 15vh;
  left: 10vw;
  transition: all 0.5s ease-in-out;
  animation: rotateFloatBigCard 6s ease-in-out infinite;
}

.card-container-right {
  position: absolute;
  top: 35vh;
  left: 38vw;
  transition: all 0.5s ease-in-out;
  animation: rotateFloatSmallCard 4s ease-in-out infinite;
}

.card {
  width: 25vw;
  height: 13vh;
  border-radius: 1vh;
  padding: 3vh;
  margin: 3vh;
  transition: transform 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
  transform: scale(1.05);
}

.big-card {
  width: 50vh;
  height: 50vh;
  background: linear-gradient(135deg, #ff512f, #dd2476);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.3);
}

.tips-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 1vh;
  padding: 1vh;
  margin: 3vh;
  height: initial;
}

.tips-card h1 {
  font-size: 2.5vh;
  padding: 0 2vh;
  color: blue;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
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
  .card-container-left {
    top: 15vh;
    left: 10vw;
  }
  .card-container-right {
    top: 35vh;
    left: 35vw;
  }
  .card {
    width: 30vw;
    height: 13vh;
  }
  .big-card {
    width: 40vh;
    height: 50vh;
  }
  .tips-card {
    height: initial;
  }
}

@media (max-width: 480px) {
  .lived2d-container {
    display: none;
  }
}
</style>
