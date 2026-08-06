// Design tokens for ChenXuBlog
// Access via useAppConfig() in components
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'rose',
      secondary: 'emerald',
      neutral: 'slate',
    },
  },
  chenxu: {
    brand: {
      rose: '#f4b3c2',
      roseLight: '#fce4e8',
      roseDark: '#d48a9e',
      gold: '#c9a87c',
      goldLight: '#e8d5b0',
      bamboo: '#6a7664',
      bambooLight: '#9db495',
      bambooDark: '#4a5644',
    },
    font: {
      display: '"Inter", "PingFang SC", sans-serif',
      mono: '"JetBrains Mono", "Fira Code", monospace',
      body: '"Noto Sans SC", "PingFang SC", sans-serif',
    },
    spacing: {
      section: '8rem',
      block: '2rem',
      element: '1rem',
    },
    animation: {
      duration: {
        fast: '0.2s',
        normal: '0.3s',
        slow: '0.6s',
        reveal: '1s',
      },
      easing: {
        smooth: 'cubic-bezier(0.25, 0.8, 0.25, 1)',
        bounce: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
        reveal: 'cubic-bezier(0.2, 0.8, 0.2, 1)',
      },
    },
    glass: {
      light: 'rgba(255, 255, 255, 0.12)',
      medium: 'rgba(255, 255, 255, 0.08)',
      heavy: 'rgba(0, 0, 0, 0.4)',
      blur: 'blur(20px)',
    },
  },
})