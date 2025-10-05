import { defineStore } from "pinia";

interface UserData {
  id: string;
  username: string;
  email: string;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isAuthenticated: false,
  }),
  actions: {
    login(userData: UserData): void {
      this.user = userData;
      this.isAuthenticated = true;
      localStorage.setItem("auth", JSON.stringify(userData));
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem("auth");
    },
  },
});
