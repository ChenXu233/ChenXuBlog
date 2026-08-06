import { defineStore } from "pinia";

interface TokenState {
  token: string | null;
  refreshToken: string | null;
}

export const useTokenStore = defineStore("token", {
  state: (): TokenState => ({
    token: localStorage.getItem("token"),
    refreshToken: localStorage.getItem("refresh_token"),
  }),

  getters: {
    getToken(): string | null {
      return this.token;
    },
    isAuthenticated(): boolean {
      return !!this.token;
    },
  },

  actions: {
    setToken(token: string | null): void {
      this.token = token;
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },
    setRefreshToken(refreshToken: string | null): void {
      this.refreshToken = refreshToken;
      if (refreshToken) {
        localStorage.setItem("refresh_token", refreshToken);
      } else {
        localStorage.removeItem("refresh_token");
      }
    },
    clearToken(): void {
      this.setToken(null);
      this.setRefreshToken(null);
    },
  },
});
