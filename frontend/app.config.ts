// Design tokens for ChenXuBlog
// Access via useAppConfig() in components
export default defineAppConfig({
  ui: {
    colors: {
      primary: "red",
      secondary: "emerald",
      neutral: "stone",
    },
  },
  chenxu: {
    brand: {
      accent: "#e3441c",
      blue: "#2638b8",
      green: "#1c6b52",
      gold: "#e8b93b",
      paper: "#f3f0e8",
    },
    font: {
      display: '"HarmonyOS Sans SC", "PingFang SC", "Helvetica Neue", Arial, sans-serif',
      mono: 'ui-monospace, "SFMono-Regular", "JetBrains Mono", Menlo, Consolas, monospace',
      body: '"HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif',
    },
    spacing: {
      section: "8rem",
      block: "2rem",
      element: "1rem",
    },
  },
});
