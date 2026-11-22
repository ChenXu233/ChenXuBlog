/**
 * 统一的 API 基址：
 * - 服务端 SSR 直连后端（NUXT_API_INTERNAL_URL）
 * - 浏览器端用同源相对路径（/apis），由 Caddy / Vite proxy 转发
 */
export function useApiBase(): string {
  const config = useRuntimeConfig();
  if (import.meta.server) {
    return String(config.apiInternal || "").replace(/\/$/, "");
  }
  return "";
}

export function useApiFetch<T>(
  path: string,
  options: Record<string, unknown> = {},
): Promise<T> {
  const base = useApiBase();
  return $fetch<T>(`${base}${path}`, options as any) as Promise<T>;
}
