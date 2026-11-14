// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },

  modules: ["@nuxt/ui", "@pinia/nuxt"],

  components: [{ path: "~/components", pathPrefix: false }],

  pinia: {
    storesDirs: ["./composables/**"],
  },

  plugins: ["~/plugins/pinia-persist.client.ts"],

  css: [
    "~/assets/css/main.css",
    "~/assets/css/pages/auth.css",
    "font-awesome/css/font-awesome.min.css",
  ],

  ssr: true,

  nitro: {
    preset: "node-server",
    devProxy: {
      "/apis": {
        // 本地默认 8001；docker dev 容器内指向 backend 服务
        target: process.env.NUXT_API_PROXY_TARGET || "http://localhost:8001",
        changeOrigin: true,
      },
    },
  },

  vite: {
    server: {
      proxy: {
        "/apis": {
          target: process.env.NUXT_API_PROXY_TARGET || "http://localhost:8001",
          changeOrigin: true,
        },
      },
    },
    ssr: {
      // vue/vue-router 打进 SSR bundle，避免 Node 22 下 CJS interop 问题
      noExternal: ["vue", "vue-router"],
    },
  },

  ui: {
    theme: {
      colors: [
        "primary",
        "secondary",
        "neutral",
        "success",
        "info",
        "warning",
        "error",
      ],
    },
  },

  // 原生暗色：默认跟随系统，用户可手动切换（右上角）
  colorMode: {
    preference: "system",
    fallback: "light",
    storageKey: "chenxu-theme",
  },

  compatibilityDate: "2025-08-06",

  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      htmlAttrs: { lang: "zh-CN" },
      title: "chenxu's homepage",
      meta: [
        {
          name: "description",
          content:
            "晨煦的个人博客：代码、物理、哲学与生活。烟花三月，雾与花之间。",
        },
        { property: "og:site_name", content: "晨煦 CHENXU" },
        { name: "theme-color", content: "#f3f0e8", media: "(prefers-color-scheme: light)" },
        { name: "theme-color", content: "#0b0c0e", media: "(prefers-color-scheme: dark)" },
      ],
      link: [
        {
          rel: "alternate",
          type: "application/rss+xml",
          title: "晨煦 CHENXU RSS",
          href: "/rss.xml",
        },
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
      ],
    },
  },

  runtimeConfig: {
    // 仅服务端使用：SSR 时直连后端（不经过外部网关）
    apiInternal:
      process.env.NUXT_API_INTERNAL_URL ||
      process.env.NUXT_API_PROXY_TARGET ||
      "http://127.0.0.1:8001",
    public: {
      apiBase: "/apis/v1",
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || "http://localhost:3000",
      githubUrl: "https://github.com/ChenXu233",
    },
  },
});
