import { defineStore } from 'pinia'
import { login as loginApi } from '@/api/auth'
import { setToken, setUserInfo, getToken, getUserInfo, removeToken, removeUserInfo } from '@/utils/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: getToken(),
    userInfo: getUserInfo()
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.userInfo?.is_admin || false,
    currentUserId: (state) => state.userInfo?.id || null
  },

  actions: {
    async login(credentials) {
      const res = await loginApi(credentials)
      this.token = res.token
      this.userInfo = res.user

      setToken(res.token)
      setUserInfo(res.user)
    },

    logout() {
      this.token = null
      this.userInfo = null
      removeToken()
      removeUserInfo()
    }
  }
})
