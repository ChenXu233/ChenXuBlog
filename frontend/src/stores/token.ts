import { defineStore } from "pinia";

interface TokenState {
  token: string | null;
}

export const useTokenStore = defineStore("token", {
  state: (): TokenState => ({
    token: localStorage.getItem("token"),
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
    clearToken(): void {
      this.setToken(null);
    },
  },
});
