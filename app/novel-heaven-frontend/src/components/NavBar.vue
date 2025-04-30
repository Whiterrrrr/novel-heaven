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
        <template v-if="!userStore.isAuthenticated">
          <router-link to="/login">Log in</router-link>
          <span>|</span>
          <router-link to="/register">Sign up</router-link>
        </template>
        <template v-else>
          <router-link to="/profile">{{ userStore.user.name }}</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/store/index';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();
const searchQuery = ref('');
const isScrolled = ref(false);

const isNovelDetailPage = computed(() => route.name === 'NovelDetail');
const isLibraryPage = computed(() => route.name === 'Library');
const isNovelContentPage = computed(() => route.name === 'NovelContent');
const grayBackgroundComputed = computed(() => isNovelDetailPage.value || isLibraryPage.value);

const search = () => {
  if (searchQuery.value.trim()) {
    router.push(`/search?q=${encodeURIComponent(searchQuery.value.trim())}`);
  }
};

function handleMyCenter() {
  if (userStore.isAuthenticated) {
    router.push('/my-center');
  } else {
    alert('Please log in or sign up to access My Center.');
  }
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

onMounted(() => window.addEventListener('scroll', handleScroll));
onBeforeUnmount(() => window.removeEventListener('scroll', handleScroll));
</script>

<style scoped>
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
</style>