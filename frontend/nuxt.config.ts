// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    '@nuxt/ui',
    '@nuxt/fonts',
    '@pinia/nuxt',
  ],

  css: ['~/assets/css/main.css'],

  ssr: true,

  nitro: {
    preset: 'node-server',
  },

  ui: {
    theme: {
      colors: {
        primary: 'rose',
        secondary: 'emerald',
        neutral: 'slate',
      },
    },
  },

  colorMode: {
    preference: 'dark',
    fallback: 'dark',
  },

  compatibilityDate: '2025-08-06',

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'ChenXuBlog',
      meta: [
        { name: 'description', content: "ChenXu's personal blog - 技术分享与生活记录" },
      ],
    },
  },

  runtimeConfig: {
    public: {
      apiBase: '/apis/v1',
    },
  },
})