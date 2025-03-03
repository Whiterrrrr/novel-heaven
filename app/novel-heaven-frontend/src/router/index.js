import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import NovelDetail from '@/views/NovelDetail.vue';
import Profile from '@/views/Profile.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/novel/:id', component: NovelDetail },
  { path: '/profile', component: Profile },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;