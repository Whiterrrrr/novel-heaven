
/* ========= main.js ========= */
import { createApp }    from 'vue';
import App              from './App.vue';
import router           from './router';
import { createPinia }  from 'pinia';
import './assets/styles.css';

import axios            from 'axios';
axios.defaults.withCredentials = true;
import { useUserStore } from '@/store/index';
import MockAdapter      from 'axios-mock-adapter';   // 保留——如果你后面有 mock 逻辑会用到

/* ========= 创建应用 ========= */
const app   = createApp(App);
const pinia = createPinia();
app.use(pinia).use(router);        // 注意：此时 **不** mount

/* ========= Axios 基址 & 拦截器 ========= */
axios.defaults.baseURL = 'http://localhost:5001';    // 按需修改

// 请求拦截器：自动把本地 token 带上
axios.interceptors.request.use(cfg => {
  const token = localStorage.getItem('token');
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
}, err => Promise.reject(err));

/* ========= 登录状态恢复后再挂载 ========= */
const userStore = useUserStore();
userStore.initAuth()          // 恢复 token（内部可异步）
  .finally(() => {
    app.mount('#app');        // 等 token 配置完再真正渲染
  });
