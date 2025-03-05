import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    isAuthenticated: false,  // 是否登录
  }),
  actions: {
    login() { this.isAuthenticated = true; },
    logout() { this.isAuthenticated = false; }
  }
});
