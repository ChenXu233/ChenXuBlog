// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: ["@nuxt/ui", "@pinia/nuxt"],

  components: [{ path: "~/components", pathPrefix: false }],

  pinia: {
    storesDirs: ["./composables/**"],
  },

  plugins: ["~/plugins/pinia-persist.client.ts"],

  css: ["~/assets/css/main.css"],

  ssr: true,

  nitro: {
    preset: "node-server",
    devProxy: {
      "/apis": {
        target: "http://localhost:8001",
        changeOrigin: true,
      },
    },
  },

  vite: {
    server: {
      proxy: {
        "/apis": {
          target: "http://localhost:8001",
          changeOrigin: true,
        },
      },
    },
    ssr: {
      // vue/vue-router 打进 SSR bundle，避免 Node 22 下 CJS interop 问题
      noExternal: ["vue", "vue-router"],
    },
  },

  fonts: {
    defaults: {
      weights: [400, 500, 600, 700],
    },
    providers: {
      google: false,
      googleicons: false,
    },
  },

  ui: {
    theme: {
      colors: {
        primary: "rose",
        secondary: "emerald",
        neutral: "slate",
      },
    },
  },

  colorMode: {
    preference: "dark",
    fallback: "dark",
  },

  compatibilityDate: "2025-08-06",

  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      title: "ChenXuBlog",
      meta: [
        {
          name: "description",
          content: "ChenXu's personal blog - 技术分享与生活记录",
        },
      ],
    },
  },

  runtimeConfig: {
    public: {
      apiBase: "/apis/v1",
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || "http://localhost:3000",
    },
  },
});
