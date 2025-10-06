import axios, { type AxiosRequestConfig, type AxiosResponse } from "axios";
import { config } from "../config/config";
import { useRouter } from "vue-router";
import { useTokenStore } from "../stores/token";

type ErrorHandler = (error: unknown) => void;
const router = useRouter();
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

service.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.status >= 400 ? Promise.reject(response) : response;
  },
  (error) => {
    error.response?.status === 502 && console.error("网关错误");
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
      errorHandler?.(error);
      throw error;
    }
  };
