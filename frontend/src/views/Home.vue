<template>
  <div class="home">
    <div class="home-content">
      <div class="home-cards-container">
        <div class="home-card-big">
          <h1>欢迎来到ChenXuBlog</h1>
        </div>
        <div class="home-cards-container-seconde">
          <div class="home-card">
            <h2>ChenXuBlog</h2>
          </div>
          <div class="home-card">
            <h2>ChenXuBlog</h2>
          </div>
          <div class="home-card">
            <h2>ChenXuBlog</h2>
          </div>
        </div>
      </div>
      <div class="home-lived-2d-container"></div>
    </div>
  </div>
</template>

<script lang="ts"></script>

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
  display: relative;
}

.home-cards-container {
  position: absolute;
  top: 15rem;
  left: 10rem;
  perspective: 600px;
}

.home-cards-container-seconde {
  position: absolute;
  top: 10rem;
  left: 30rem;
  perspective: 800px;
}

.home-card-big,
.home-card {
  width: 30rem;
  height: 10rem;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 20px;
  margin: 20px;
  animation: rotateFloatSmallCard 4s ease-in-out infinite;
}

.home-card-big {
  width: 40rem;
  height: 40rem;
  animation: rotateFloatBigCard 6s ease-in-out infinite;
}

@keyframes rotateFloatBigCard {
  0% {
    transform: translateY(0) rotateY(15deg);
  }
  50% {
    transform: translateY(-20px) rotateY(15deg);
  }
  100% {
    transform: translateY(0) rotateY(15deg);
  }
}

@keyframes rotateFloatSmallCard {
  0% {
    transform: translateY(0) rotateY(-15deg);
  }
  50% {
    transform: translateY(-20px) rotateY(-15deg);
  }
  100% {
    transform: translateY(0) rotateY(-15deg);
  }
}

@media (max-width: 768px) {
  .home {
    background-image: url("/yunxi.jpg");
    background-position: center top;
  }
  .home-cards-container {
    top: 10rem;
    left: 1rem;
  }
  .home-cards-container-seconde {
    top: 10rem;
    left: 20rem;
  }
  .home-card-big,
  .home-card {
    width: 20rem;
    height: 10rem;
  }
  .home-card-big {
    width: 30rem;
    height: 30rem;
  }
}

@media (max-width: px) {
  .home-lived-2d-container {
    display: none;
  }
}
</style>
