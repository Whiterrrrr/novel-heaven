<template>
  <nav class="navbar">
    <!-- Logo -->
    <div class="nav-left">
        <span>Novel Heaven</span>
      
    </div>

    <!-- 导航，搜索框 ，用户登录 -->
    <div class="nav-right">
      <div class="nav-links">
        <router-link to="/" style="font-weight: bold;">Home</router-link>
        <span>  </span>
        <router-link to="/library">Library</router-link>
        <span>  </span>
        <router-link to="/bookshelf">Bookshelf</router-link>
        <span>  </span>
        <router-link to="/author">Author Section</router-link>
      </div>

      <!-- 搜索框 -->
      <div class="nav-search">
        <input type="text" v-model="searchQuery" placeholder="searching novel or author" />
        <button @click="search">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 16 16">
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.099zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
          </svg>
        </button>
      </div>

      <!-- 用户登录 / 用户中心 -->
      <div class="nav-user">
        <template v-if="!userStore.isAuthenticated">
          <router-link to="/login">Log in</router-link>
          <span>|</span>
          <router-link to="/register">Sign up</router-link>
        </template>
        <template v-else>
          <router-link to="/profile">Profile</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/store/index';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const searchQuery = ref('');
const router = useRouter();

const search = () => {
  if (searchQuery.value.trim()) {
    router.push(`/search?q=${searchQuery.value}`);
  }
};
</script>

<style scoped>
/* 整体导航栏 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background: transparent; 
  width:95%;
  z-index: 1000;
  position: absolute;
}

/* 左侧 Logo */
.nav-left {
  display: flex;
  align-items: center;
  font-size: 30px;
  font-family:"Brush Script MT",cursive;
}


/* 右侧 导航 + 搜索 + 用户登录 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 40px;
}

/* 导航菜单 */
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

/* 线条从中间展开 */
.nav-links a:hover::after {
  width: 100%;
  left: 0;
}

/* 搜索框 */
/* 搜索框容器 */
.nav-search {
  display: flex;
  align-items: center;
  background: #fdf8f2; 
  border-radius: 25px; 
  overflow: hidden;
  padding: 3px 13px; 
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); 
}

/* 输入框 */
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

/* 搜索按钮 */
.nav-search button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 5px;
}

/* 搜索按钮的图标 */
.nav-search button svg {
  fill: #666; 
  width: 18px;
  height: 18px;
}
/* 用户中心 / 登录注册 */
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

