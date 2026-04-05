import { defineStore } from "pinia";

interface PermissionState {
  permissions: string[];
}

export const usePermissionStore = defineStore("permission", {
  state: (): PermissionState => ({
    permissions: [],
  }),

  getters: {
    hasPermission: (state) => (permission: string): boolean => {
      return state.permissions.includes(permission);
    },
    isSuperUser: (state): boolean => {
      return state.permissions.includes("blog:create");
    },
  },

  actions: {
    setPermissions(permissions: string[]) {
      this.permissions = permissions;
    },
    addPermission(permission: string) {
      if (!this.permissions.includes(permission)) {
        this.permissions.push(permission);
      }
    },
    clearPermissions() {
      this.permissions = [];
    },
  },
});
