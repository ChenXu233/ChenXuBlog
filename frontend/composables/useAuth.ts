// Unified auth store — merges old authStore + tokenStore + permissionStore
import { defineStore } from "#imports";
import type { UserResponse } from "~/shared/api-client/types.gen";
import { authService } from "~/service/auth";
import { userService } from "~/service/user";
import { permissionService } from "~/service/permission";

interface AuthState {
  token: string | null;
  refreshToken: string | null;
  user: UserResponse | null;
  permissions: string[];
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    token: null,
    refreshToken: null,
    user: null,
    permissions: [],
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    hasPermission: (state) => (permission: string) =>
      state.permissions.includes(permission),
    isAdmin: (state) => state.permissions.includes("admin:access"),
  },

  actions: {
    async login(evidence: string, password: string) {
      const data = await authService.login(evidence, password);
      this.token = data.access_token;
      try {
        const refreshed = await authService.refreshToken();
        if (refreshed) this.token = refreshed;
      } catch {
        // refresh via cookie failed, that's okay
      }
      await this.fetchUserInfo();
      await this.fetchPermissions();
    },

    async register(username: string, email: string, password: string) {
      await authService.register({ username, email, password });
    },

    async fetchUserInfo() {
      if (!this.token) return;
      try {
        this.user = await userService.getOwnInfo();
      } catch {
        // token might be expired
      }
    },

    async fetchPermissions() {
      if (!this.token) return;
      try {
        const data = await permissionService.getPermissions();
        this.permissions = data.permissions;
      } catch {
        this.permissions = [];
      }
    },

    logout() {
      this.token = null;
      this.refreshToken = null;
      this.user = null;
      this.permissions = [];
      navigateTo("/login");
    },
  },

  persist: {
    key: "chenxu-auth",
    storage: typeof localStorage !== "undefined" ? localStorage : undefined,
  },
});
