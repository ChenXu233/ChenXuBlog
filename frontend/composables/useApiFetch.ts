// API fetch wrapper: SSR uses backend directly, client uses vite proxy
// Fixes Nuxt SSR treating relative /apis paths as router navigation
import type { UseFetchOptions } from "#app";

const API_BASE = "/apis/v1";

function resolveUrl(url: string): string {
  if (import.meta.server) {
    // SSR: call backend directly
    const backend =
      process.env.NUXT_API_INTERNAL_URL || "http://127.0.0.1:8001";
    return url.startsWith("http")
      ? url
      : `${backend}${API_BASE}${url.startsWith("/") ? url : "/" + url}`;
  }
  return url.startsWith("http")
    ? url
    : `${API_BASE}${url.startsWith("/") ? url : "/" + url}`;
}

export function useApiFetch<T>(
  url: string | (() => string),
  opts: UseFetchOptions<T> = {},
) {
  const resolved =
    typeof url === "function" ? () => resolveUrl(url()) : resolveUrl(url);
  return useFetch<T>(resolved, {
    ...opts,
    // 客户端绕过 vite proxy 优化，避免缓存旧数据
    ...(import.meta.client
      ? { key: typeof url === "string" ? url : "dynamic" }
      : {}),
  });
}
