<script setup lang="ts"></script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-100 text-gray-800">
    <!-- Header -->
    <header class="bg-green-500 text-white py-4 px-8 text-center">
      <h1 class="text-4xl font-bold">ChenXu Blog</h1>
      <nav>
        <ul class="flex justify-center gap-6 mt-4">
          <li>
            <a href="#home" class="hover:underline font-semibold">Home</a>
          </li>
          <li>
            <a href="#about" class="hover:underline font-semibold">About</a>
          </li>
          <li>
            <a href="#posts" class="hover:underline font-semibold">Posts</a>
          </li>
          <li>
            <a href="#contact" class="hover:underline font-semibold">Contact</a>
          </li>
        </ul>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="flex-1 p-8">
      <section class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-2xl font-bold text-green-500">Welcome to My Blog</h2>
        <p class="mt-4">
          This is a simple blog page built with Vue 3 and Vite. Explore the
          posts, learn something new, and enjoy your stay!
        </p>
      </section>
      <section class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-bold text-green-500">Latest Post</h2>
        <p class="mt-4">
          Stay tuned for the latest updates and articles. This is where the most
          recent blog post will appear.
        </p>
      </section>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white text-center py-4">
      <p>&copy; 2025 ChenXu Blog. All rights reserved.</p>
    </footer>
  </div>
</template>
