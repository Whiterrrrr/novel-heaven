import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import NovelDetail from '@/views/NovelDetail.vue';
import Profile from '@/views/Profile.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Library from '@/views/Library.vue';
import NovelContent from '@/views/NovelContent.vue';
import Search  from '@/views/Search.vue';
const routes = [
  { path: '/', component: Home },
  { path: '/search', component: Search, name: 'Search' },
  { path: '/novel/:id', component: NovelDetail, name:"NovelDetail"},
  { path: '/profile', component: Profile },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/library', component: Library, name:"Library" },
  { path: '/novel/:id/content/:chapterId', component: NovelContent, name:"NovelContent" },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;