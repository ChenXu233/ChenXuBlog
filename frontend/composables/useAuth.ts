// Unified auth store — merges old authStore + tokenStore + permissionStore
import { defineStore } from 'pinia'
import type { User, UserLoginResponse } from '~/types/user'

interface AuthState {
  token: string | null
  refreshToken: string | null
  user: User | null
  permissions: string[]
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: null,
    refreshToken: null,
    user: null,
    permissions: [],
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    hasPermission: (state) => (permission: string) => state.permissions.includes(permission),
    isAdmin: (state) => state.permissions.includes('admin:access'),
  },

  actions: {
    async login(evidence: string, password: string) {
      const data = await $fetch<UserLoginResponse>('/apis/v1/auth/login', {
        method: 'POST',
        body: { evidence, password },
      })
      this.token = data.access_token
      try {
        const refresh = await $fetch<{ access_token: string }>('/apis/v1/auth/refresh', {
          method: 'POST',
        })
        this.token = refresh.access_token
      } catch {
        // refresh via cookie failed, that's okay
      }
      await this.fetchUserInfo()
      await this.fetchPermissions()
    },

    async register(username: string, email: string, password: string) {
      await $fetch('/apis/v1/auth/register', {
        method: 'POST',
        body: { username, email, password },
      })
    },

    async fetchUserInfo() {
      if (!this.token) return
      try {
        const data = await $fetch<User>('/apis/v1/user/info', {
          headers: { Authorization: `Bearer ${this.token}` },
        })
        this.user = data
      } catch {
        // token might be expired
      }
    },

    async fetchPermissions() {
      if (!this.token) return
      try {
        const data = await $fetch<{ permissions: string[] }>('/apis/v1/permission/', {
          headers: { Authorization: `Bearer ${this.token}` },
        })
        this.permissions = data.permissions
      } catch {
        this.permissions = []
      }
    },

    logout() {
      this.token = null
      this.refreshToken = null
      this.user = null
      this.permissions = []
      navigateTo('/login')
    },
  },

  persist: {
    storage: 'localStorage',
    key: 'chenxu-auth',
  },
})