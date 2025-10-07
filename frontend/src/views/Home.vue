<template>
  <div class="home">
    <div class="home-content">
      <div class="home-cards-container">
        <div class="home-card-big">
          <h1>欢迎来到ChenXuBlog</h1>
        </div>
        <div class="home-card">
          <h2>ChenXuBlog</h2>
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
  transition: all 0.7s ease;
}

.home-content {
  display: relative;
  perspective: 800px;
}

.home-cards-container {
  position: absolute;
  top: 10rem;
  left: 10rem;
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
}

.home-card-big,
.home-card {
  width: 10rem;
  height: 10rem;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 20px;
  margin: 20px;
}

.home-card-big {
  width: 30rem;
  height: 30rem;
}

@media (max-width: 768px) {
  .home {
    background-image: url("/yunxi.jpg");
    background-position: center top;
  }
}
</style>
