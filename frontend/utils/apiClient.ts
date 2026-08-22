// 统一 API client：baseUrl + Bearer 注入 + 401 自动刷新重试
import { client } from "../shared/api-client/client.gen";

// SDK 生成的 url 已含 /apis/v1 前缀，baseUrl 留空避免重复
client.setConfig({ baseUrl: "" });

let accessToken: string | null = null;

export const setAccessToken = (token: string | null) => {
  accessToken = token;
};

export const getAccessToken = () => accessToken;

// 请求拦截器：注入 Bearer
client.interceptors.request.use((request) => {
  if (accessToken) {
    request.headers.set("Authorization", `Bearer ${accessToken}`);
  }
  return request;
});

// 刷新中避免并发重复刷新
let refreshing: Promise<string | null> | null = null;

const doRefresh = async (): Promise<string | null> => {
  try {
    // refresh_token 是 httpOnly cookie，浏览器自动携带
    const { data } = await client.post({
      url: "/apis/v1/auth/refresh",
    });
    const token =
      data && typeof data === "object" && "access_token" in data
        ? (data as { access_token: string }).access_token
        : null;
    setAccessToken(token);
    return token;
  } catch {
    setAccessToken(null);
    return null;
  }
};

const refreshToken = () => {
  if (!refreshing) refreshing = doRefresh().finally(() => (refreshing = null));
  return refreshing;
};

// 通用调用封装：401 时刷新并重试一次
export const apiCall = async <T>(
  fn: () => Promise<{ data?: T; error?: any }>,
): Promise<T> => {
  let result = await fn();
  if (
    result.error &&
    (result.error.status === 401 || result.error.statusCode === 401)
  ) {
    const newToken = await refreshToken();
    if (newToken) result = await fn();
  }
  if (result.error) {
    const err = new Error(
      result.error.detail || result.error.message || "请求失败",
    );
    (err as any).status = result.error.status ?? result.error.statusCode;
    throw err;
  }
  return result.data as T;
};
