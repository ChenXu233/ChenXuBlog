import axios, {
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios";
import { config } from "../config/config.ts";
import { useTokenStore } from "../stores/token";

const service: AxiosInstance = axios.create({
  baseURL: config.BackendUrl as string,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json;charset=utf-8",
  },
});

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const tokenStore = useTokenStore();
    const token = tokenStore.getToken;

    if (token) {
      config.headers = config.headers || {};
      config.headers["token"] = `${token}`;
    }

    return config;
  },
  (error) => {
    // 处理请求错误
    console.error("请求错误:", error);
    return Promise.reject(error);
  },
);

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 2xx范围内的状态码都会触发该函数
    // 对响应数据做点什么
    console.log("响应数据:", response.data);
    const res = response.data;
    // 这里可以根据后端返回的数据结构进行统一处理
    // 例如：判断code是否为成功状态
    if (res.code && res.code !== 200) {
      // 提示错误信息
      console.error("请求失败:", res.message || "未知错误");
      return Promise.reject(new Error(res.message || "未知错误"));
    }
    return res;
  },
  (error) => {
    // 超出2xx范围的状态码都会触发该函数
    // 处理响应错误
    console.error("响应错误:", error);
    // 可以根据错误状态码做一些处理
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，跳转到登录页
          console.error("未授权，请重新登录");
          // 这里可以添加跳转到登录页的逻辑
          break;
        case 403:
          console.error("拒绝访问");
          break;
        case 404:
          console.error("请求地址不存在");
          break;
        case 500:
          console.error("服务器错误");
          break;
        default:
          console.error("请求失败");
      }
    }
    return Promise.reject(error);
  },
);

// 导出常用的请求方法
export const request = {
  // GET请求
  get<T = any>(
    url: string,
    params?: any,
    config?: AxiosRequestConfig,
  ): Promise<T> {
    return service.get(url, { params, ...config });
  },

  // POST请求
  post<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
  ): Promise<T> {
    return service.post(url, data, config);
  },

  // PUT请求
  put<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
  ): Promise<T> {
    return service.put(url, data, config);
  },

  // DELETE请求
  delete<T = any>(
    url: string,
    params?: any,
    config?: AxiosRequestConfig,
  ): Promise<T> {
    return service.delete(url, { params, ...config });
  },

  // 上传文件
  upload<T = any>(
    url: string,
    file: File,
    config?: AxiosRequestConfig,
  ): Promise<T> {
    const formData = new FormData();
    formData.append("file", file);
    return service.post(url, formData, {
      headers: { "Content-Type": "multipart/form-data" },
      ...config,
    });
  },
};

export default service;
