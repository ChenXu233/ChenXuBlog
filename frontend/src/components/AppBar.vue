<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center space-x-4">
          <router-link to="/" class="text-gray-800 text-lg font-semibold">
            首页
          </router-link>
          <router-link to="/about" class="text-gray-800 text-lg font-semibold">
            关于
          </router-link>
          <router-link
            to="/contact"
            class="text-gray-800 text-lg font-semibold"
          >
            联系我们
          </router-link>
        </div>
        <router-link to="/" class="text-2xl font-bold text-gray-800">
          My Blog
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "AppBar",
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
