// Auth-aware fetch: loads when token is available (client-side only)
import type { Ref } from "vue";

export function useAuthFetch<T>(
  url: string | (() => string),
  opts: { watch?: Ref[] } = {},
) {
  const auth = useAuthStore();
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const pending = ref(false);
  let requestId = 0;

  async function load() {
    if (!auth.token) return;
    const id = ++requestId;
    pending.value = true;
    try {
      const u = typeof url === "function" ? url() : url;
      const res = await $fetch<T>(u, {
        headers: { Authorization: `Bearer ${auth.token}` },
      });
      if (id === requestId) data.value = res;
    } catch (e: any) {
      if (id === requestId) {
        error.value = e;
        if (e?.status === 401) auth.logout();
      }
    } finally {
      if (id === requestId) pending.value = false;
    }
  }

  // 客户端：token 就绪立即加载（watch 覆盖 persist hydrate 的时序）
  if (import.meta.client) {
    watch(
      () => auth.token,
      (token) => {
        if (token) load();
      },
      { immediate: true },
    );
  }

  if (opts.watch) {
    for (const ref of opts.watch) {
      watch(ref, () => load());
    }
  }

  return { data, error, pending, refresh: load };
}
