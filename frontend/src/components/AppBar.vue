<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="text-2xl font-bold text-gray-800">
          My Blog
        </router-link>
        <!-- 导航链接（桌面端显示，移动端隐藏） -->
        <div class="hidden md:flex items-center space-x-4">
          <router-link
            to="/"
            class="text-gray-800 text-lg font-semibold hover:text-blue-500 transition duration-300"
          >
            首页
          </router-link>
          <router-link
            to="/about"
            class="text-gray-800 text-lg font-semibold hover:text-blue-500 transition duration-300"
          >
            关于
          </router-link>
          <router-link
            to="/contact"
            class="text-gray-800 text-lg font-semibold hover:text-blue-500 transition duration-300"
          >
            联系我们
          </router-link>
        </div>
        <!-- 汉堡菜单按钮（移动端显示） -->
        <button
          class="md:hidden text-gray-800 focus:outline-none"
          @click="toggleMenu"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            ></path>
          </svg>
        </button>
      </div>
    </div>
    <!-- 移动端菜单（点击汉堡菜单时显示） -->
    <div v-if="isMenuOpen" class="md:hidden bg-white shadow-lg">
      <router-link
        to="/"
        class="block px-4 py-2 text-gray-800 text-lg font-semibold hover:bg-gray-100"
      >
        首页
      </router-link>
      <router-link
        to="/about"
        class="block px-4 py-2 text-gray-800 text-lg font-semibold hover:bg-gray-100"
      >
        关于
      </router-link>
      <router-link
        to="/contact"
        class="block px-4 py-2 text-gray-800 text-lg font-semibold hover:bg-gray-100"
      >
        联系我们
      </router-link>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  name: "AppBar",
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
  },
});
</script>

<style scoped>
/* 可根据需要添加额外的自定义样式 */
</style>
