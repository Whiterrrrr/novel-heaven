<template>
  <nav
    v-if="!isNovelContentPage"
    class="navbar nav-default"
    :class="{ scrolled: isScrolled, grayBackground: grayBackgroundComputed }"
  >
    <!-- Logo -->
    <div class="nav-left">
      <span>Novel Heaven</span>
    </div>

    <!-- Links + search + user -->
    <div class="nav-right">
      <!-- 导航链接 -->
      <div class="nav-links">
        <router-link to="/" class="home-link">Home</router-link>
        <router-link to="/library">Library</router-link>
        <a href="#" @click.prevent="handleMyCenter">My Center</a>
      </div>

      <!-- 搜索框 -->
      <div class="nav-search">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="search novel or author"
        />
        <button @click="search">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 16 16">
            <path
              d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.099zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"
            />
          </svg>
        </button>
      </div>

      <!-- 登录 / 用户名 -->
      <div class="nav-user">
        <!-- 未登录 -->
        <template v-if="!userStore.isAuthenticated">
          <router-link to="/login">Log in</router-link><span>|</span>
          <router-link to="/register">Sign up</router-link>
        </template>

        <!-- 已登录 -->
        <template v-else>
          <span>{{ userStore.user.name }}</span>
          <button class="logout-btn" @click="userStore.logout">Log out</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, onBeforeMount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/store/index';
import axios from 'axios';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const searchQuery = ref('');
const isScrolled = ref(false);

// 页签判断
const isNovelDetailPage = computed(() => route.name === 'NovelDetail');
const isLibraryPage    = computed(() => route.name === 'Library');
const isNovelContentPage = computed(() => route.name === 'NovelContent');
const grayBackgroundComputed = computed(
  () => isNovelDetailPage.value || isLibraryPage.value
);

// 搜索跳转
const search = () => {
  const q = searchQuery.value.trim();
  if (q) router.push(`/search?q=${encodeURIComponent(q)}`);
};

// 我的中心
function handleMyCenter() {
  if (userStore.isAuthenticated) router.push('/my-center');
  else alert('Please log in or sign up to access My Center.');
}

// 后端登出 + 前端清理
async function logout() {
  try {
    await axios.post(
      '/api/author/logout',
      {},
      { headers: { Authorization: `Bearer ${localStorage.token}` } }
    );
  } catch (err) {
    console.warn('Logout API failed:', err);
  }
  localStorage.removeItem('token');
  userStore.isAuthenticated = false;
  router.push('/login');
}

// 滚动样式
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

/**
 * 新增：页面刷新或首次加载时调用
 * 如果本地有 token，就向后端 /api/author/me 验证并更新 userStore.isAuthenticated
 */
async function checkAuth() {
  const token = localStorage.getItem('token');
  if (!token) {
    userStore.isAuthenticated = false;
    return;
  }
  try {
    // 请求用户信息，成功视作已登录
    await axios.get('/api/author/me', {
      headers: { Authorization: `Bearer ${token}` }
    });
    userStore.isAuthenticated = true;
  } catch {
    // token 无效或过期
    localStorage.removeItem('token');
    userStore.isAuthenticated = false;
  }
}

// 在挂载前先校验登录状态
onBeforeMount(() => {
  checkAuth();
});

// 挂载滚动监听
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

// 卸载时移除
onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
/* 保持原有全部样式，只补一个 logout 按钮样式 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background: transparent;
  width: 100%;
  z-index: 1000;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  transition: background-color 0.3s ease;
}
.navbar.scrolled {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.navbar.grayBackground {
  background-color: #f5f5f5;
  box-shadow: none;
}
.nav-left {
  display: flex;
  align-items: center;
  font-size: 30px;
  font-family: "Brush Script MT", cursive;
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 40px;
  margin-right: 50px;
}
.nav-links {
  display: flex;
  gap: 15px;
}
.nav-links a {
  position: relative;
  text-decoration: none;
  font-size: 14px;
  color: black;
}
.nav-links .home-link,
.nav-links a.router-link-active {
  font-weight: bold;
}
.nav-links a::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 0;
  height: 2px;
  background-color: black;
  transition: all 0.3s ease-out;
}
.nav-links a:hover::after {
  width: 100%;
  left: 0;
}
.nav-search {
  display: flex;
  align-items: center;
  background: #fdf8f2;
  border-radius: 25px;
  overflow: hidden;
  padding: 3px 13px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.nav-search input {
  border: none;
  background: transparent;
  font-size: 10px;
  color: #666;
  flex: 1;
  outline: none;
}
.nav-search input::placeholder {
  color: #c8bfb2;
}
.nav-search button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 5px;
}
.nav-search button svg {
  fill: #666;
  width: 18px;
  height: 18px;
}
.nav-user {
  display: flex;
  align-items: center;
  gap: 10px;
}
.nav-user a {
  color: black;
  text-decoration: none;
  font-size: 14px;
}
.nav-user a:hover {
  color: #ff6600;
}
.nav-user span {
  color: #999;
}
.logout-btn{border:none;background:transparent;color:#ff6600;font-size:14px;cursor:pointer}
.logout-btn:hover{text-decoration:underline}
</style>
