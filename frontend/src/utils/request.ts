import axios, { type AxiosResponse, type AxiosRequestConfig } from "axios";
import { config } from "../config/config";
import { useTokenStore } from "../stores/token";
import { createApp, h } from "vue";
import Error from "../components/Error.vue";

// 创建错误组件实例的函数
export const showError = (
  message: string,
  title?: string,
  type?: "error" | "warning" | "info" | "success",
  onRetry?: () => void,
) => {
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

type ErrorHandler = (error: unknown) => void;
const tokenStore = useTokenStore();

const service = axios.create({
  baseURL: config.BackendUrl,
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

service.interceptors.request.use(
  (config) => {
    const token = tokenStore.token;
    token && (config.headers.token = `${token}`);
    return config;
  },
  (error) => Promise.reject(error),
);

// 自动错误处理函数
const handleError = (error: unknown) => {
  let errorMessage = "请求失败，请稍后重试";
  let errorTitle = "网络错误";

  if (typeof error === "object" && error !== null) {
    // 先检查是否有response对象（Axios错误）
    const errorObj = error as any;
    if (errorObj.response) {
      // 处理HTTP响应错误
      const { status, data } = errorObj.response;

      switch (status) {
        case 401:
          errorTitle = "未授权";
          errorMessage = data?.detail || "您需要先登录才能访问该资源";
          break;
        case 403:
          errorTitle = "拒绝访问";
          errorMessage = data?.detail || "您没有权限访问该资源";
          break;
        case 404:
          errorTitle = "资源不存在";
          errorMessage = data?.detail || "请求的资源不存在";
          break;
        case 500:
          errorTitle = "服务器错误";
          errorMessage = data?.detail || "服务器内部错误，请稍后重试";
          break;
        case 502:
          errorTitle = "网关错误";
          errorMessage = data?.detail || "服务器暂时无法响应，请稍后重试";
          break;
        default:
          errorTitle = "请求失败";
          errorMessage = data?.detail || `HTTP错误 ${status}`;
      }
    } else if (errorObj.request) {
      // 请求发出但没有收到响应
      errorTitle = "网络错误";
      errorMessage = "无法连接到服务器，请检查网络连接";
    } else {
      // 其他类型的错误
      errorMessage = String(errorObj);
    }
  } else {
    // 处理原始类型错误
    errorMessage = String(error);
  }

  // 显示错误弹窗
  showError(errorMessage, errorTitle, "error");
};

service.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.status >= 400 ? Promise.reject(response) : response;
  },
  (error) => {
    // 自动显示错误弹窗
    handleError(error);
    return Promise.reject(error);
  },
);

export const request = <T>(config: AxiosRequestConfig) =>
  service.request<T>(config);

export const get = <T>(url: string, params?: object) =>
  request<T>({ method: "get", url, params });

export const post = <T>(url: string, data?: object) =>
  request<T>({ method: "post", url, data });

export const createApiRequest =
  (errorHandler?: ErrorHandler) =>
  async <T>(config: AxiosRequestConfig) => {
    try {
      return await request<T>(config);
    } catch (error) {
      if (errorHandler) {
        errorHandler(error);
      } else {
        handleError(error);
      }
      throw error;
    }
  };
