<script setup lang="ts"></script>

<template>
  <div class="blog-container">
    <!-- Header -->
    <header class="blog-header">
      <h1>ChenXu Blog</h1>
      <nav>
        <ul class="nav-links">
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#posts">Posts</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="blog-main">
      <section class="blog-post">
        <h2>Welcome to My Blog</h2>
        <p>
          This is a simple blog page built with Vue 3 and Vite. Explore the
          posts, learn something new, and enjoy your stay!
        </p>
      </section>
      <section class="blog-post">
        <h2>Latest Post</h2>
        <p>
          Stay tuned for the latest updates and articles. This is where the most
          recent blog post will appear.
        </p>
      </section>
    </main>

    <!-- Footer -->
    <footer class="blog-footer">
      <p>&copy; 2025 ChenXu Blog. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
/* General Styles */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background-color: #f9f9f9;
  color: #333;
}

.blog-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header Styles */
.blog-header {
  background-color: #42b883;
  color: white;
  padding: 1em 2em;
  text-align: center;
}

.blog-header h1 {
  margin: 0;
  font-size: 2.5em;
}

.nav-links {
  list-style: none;
  padding: 0;
  margin: 1em 0 0;
  display: flex;
  justify-content: center;
  gap: 1.5em;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-links a:hover {
  text-decoration: underline;
}

/* Main Content Styles */
.blog-main {
  flex: 1;
  padding: 2em;
}

.blog-post {
  background: white;
  margin: 1em 0;
  padding: 1.5em;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.blog-post h2 {
  margin-top: 0;
  color: #42b883;
}

/* Footer Styles */
.blog-footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1em 0;
}
</style>
