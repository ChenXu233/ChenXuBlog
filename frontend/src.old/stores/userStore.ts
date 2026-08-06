import { defineStore } from "pinia";
import { useAuthStore } from "./authStore";

// 兼容层：将 userStore 作为 authStore 的便捷访问器
// 所有用户信息现在由 authStore 统一管理
export const useUserStore = defineStore("user", {
  state: () => ({}),

  getters: {
    id: (): string => {
      const authStore = useAuthStore();
      return authStore.currentUser?.uuid || "";
    },
    name: (): string => {
      const authStore = useAuthStore();
      return authStore.username;
    },
    avatar_url: (): string => {
      const authStore = useAuthStore();
      return authStore.avatarUrl;
    },
  },

  actions: {
    // 保留此方法以兼容，但重定向到 authStore
    setUserInfo(payload: { id: string; name: string }) {
      const authStore = useAuthStore();
      if (authStore.currentUser) {
        authStore.currentUser.uuid = payload.id;
        authStore.currentUser.username = payload.name;
      }
    },
  },
});
