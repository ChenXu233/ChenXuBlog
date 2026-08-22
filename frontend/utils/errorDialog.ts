// 错误提示弹窗
import { createApp, h } from "vue";
import Error from "../components/common/Error.vue";

export const showErrorDialog = (
  message: string,
  title?: string,
  type?: "error" | "warning" | "info" | "success",
  onRetry?: () => void,
) => {
  if (!import.meta.client) return () => {};
  // 创建挂载容器
  const container = document.createElement("div");
  document.body.appendChild(container);

  // 创建应用实例
  const app = createApp({
    render: () =>
      h(Error, {
        message,
        title,
        type,
        onRetry,
        onClose: () => {
          app.unmount();
          document.body.removeChild(container);
        },
      }),
  });

  // 挂载应用
  app.mount(container);

  // 返回卸载函数
  return () => {
    app.unmount();
    document.body.removeChild(container);
  };
};
