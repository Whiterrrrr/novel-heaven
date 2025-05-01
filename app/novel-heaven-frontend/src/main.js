import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import './assets/styles.css';
import axios from 'axios';
import { useUserStore } from '@/store/index';
import MockAdapter from 'axios-mock-adapter';

/* ========= Vue / Pinia ========= */
const app   = createApp(App);
const pinia = createPinia();
app.use(pinia).use(router).mount('#app');

/* ========= Axios 默认基址 ========= */
axios.defaults.baseURL = 'https://api.novel-heaven.com'; // 按需修改

/* ========= 登录状态恢复 ========= */
const userStore = useUserStore();
userStore.initAuth();

