import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useUserStore = defineStore("user", {
  state: () => ({
    isAuthenticated: false,
    user: null,          // { id, name, email }
  }),
  actions: {
    /* 登录后调用 */
    login(userObj, token) {
      this.user = userObj;
      this.isAuthenticated = true;
      localStorage.setItem("token", token);
      axios.defaults.headers.common.Authorization = `Bearer ${token}`;
    },
    /* 退出登录 */
    logout() {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem("token");
      delete axios.defaults.headers.common.Authorization;
      const router = useRouter();
      router.push("/");           // 可改成 /login
    },
    /* APP 启动时调用：从 localStorage 恢复登录态 */
    async initAuth() {
      const token = localStorage.getItem("token");
      if (!token) return;
      try {
        axios.defaults.headers.common.Authorization = `Bearer ${token}`;
        const { data } = await axios.get("/api/me"); // 获取当前用户资料
        this.user = data.user;                       // { id, name, email }
        this.isAuthenticated = true;
      } catch {
        this.logout(); // token 失效
      }
    },
  },
});
