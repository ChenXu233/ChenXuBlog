import { defineStore } from "pinia";
import { get } from "../utils/request";
import type { User } from "../types/user";
import { useTokenStore } from "./token";
import { usePermissionStore } from "./permission";

interface AuthUser {
  uuid: string;
  username: string;
  email: string;
  avatar_url: string;
}

interface AuthState {
  user: AuthUser | null;
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => {
    // 从 localStorage 恢复用户信息
    const storedUser = localStorage.getItem("user");
    return {
      user: storedUser ? JSON.parse(storedUser) : null,
    };
  },

  getters: {
    isAuthenticated: (state): boolean => {
      const tokenStore = useTokenStore();
      return tokenStore.isAuthenticated && state.user !== null;
    },
    currentUser: (state): AuthUser | null => state.user,
    avatarUrl: (state): string => state.user?.avatar_url || "",
    username: (state): string => state.user?.username || "Guest",
  },

  actions: {
    setUser(user: AuthUser) {
      this.user = user;
      localStorage.setItem("user", JSON.stringify(user));
    },

    clearUser() {
      this.user = null;
      localStorage.removeItem("user");
    },

    async login(accessToken: string, refreshToken: string | undefined) {
      const tokenStore = useTokenStore();
      const permissionStore = usePermissionStore();

      // 设置 token
      tokenStore.setToken(accessToken);
      if (refreshToken) {
        tokenStore.setRefreshToken(refreshToken);
      }

      // 加载权限
      try {
        const res = await get<{ permissions: string[] }>("/permission/");
        permissionStore.setPermissions(res.data.permissions);
      } catch {
        permissionStore.clearPermissions();
      }
    },

    logout() {
      const tokenStore = useTokenStore();
      const permissionStore = usePermissionStore();

      tokenStore.clearToken();
      permissionStore.clearPermissions();
      this.clearUser();
    },

    async fetchUserInfo() {
      const res = await get<User>("/user/info");
      this.setUser({
        uuid: res.data.uuid,
        username: res.data.username,
        email: res.data.email,
        avatar_url: res.data.avatar_url || "",
      });
    },
  },
});
