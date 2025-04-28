import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import './assets/styles.css';
import axios from 'axios';
import { useUserStore } from "@/store/index";

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount('#app');
const userStore = useUserStore();
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  userStore.setToken(token);    // 视你的 store 而定：把 token 存到 Pinia/Vuex
}
