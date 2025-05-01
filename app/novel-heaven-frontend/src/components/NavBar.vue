<template>
  <nav class="navbar">
    <!-- Logo -->
    <div class="nav-left"><span>Novel Heaven</span></div>

    <div class="nav-right">
      <!-- 链接 -->
      <div class="nav-links">
        <router-link to="/" style="font-weight:bold">Home</router-link>
        <router-link to="/library">Library</router-link>
        <a href="#" @click.prevent="handleMyCenter">My Center</a>
      </div>

      <!-- 搜索 -->
      <div class="nav-search">
        <input v-model="keyword" placeholder="searching novel or author" />
        <button @click="search">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 16 16">
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398l3.85 3.85 1.415-1.414-3.85-3.85zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
          </svg>
        </button>
      </div>

      <!-- 登录 / 登出 -->
      <div class="nav-user">
        <!-- 未登录 -->
        <template v-if="!auth.isAuthenticated">
          <router-link to="/login">Log in</router-link><span>|</span>
          <router-link to="/register">Sign up</router-link>
        </template>

        <!-- 已登录 -->
        <template v-else>
          <span>{{ auth.user.name }}</span>
          <button class="logout-btn" @click="auth.logout">Log out</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/user';

const router   = useRouter();
const auth     = useUserStore();
const keyword  = ref('');

function search() {
  if (keyword.value.trim()) router.push(`/search?q=${keyword.value.trim()}`);
}

function handleMyCenter() {
  if (auth.isAuthenticated) router.push('/my-center');
  else alert('Please log in or sign up to access My Center.');
}
</script>

<style scoped>
/* 维持原先样式 + 登出按钮 */
.navbar{display:flex;justify-content:space-between;align-items:center;padding:10px 20px;background:transparent;width:95%;z-index:1000;position:absolute}
.nav-left{font-size:30px;font-family:"Brush Script MT",cursive}
.nav-right{display:flex;align-items:center;gap:40px}
.nav-links{display:flex;gap:15px}
.nav-links a{position:relative;font-size:14px;color:black;text-decoration:none}
.nav-links a.router-link-active{font-weight:bold}
.nav-links a::after{content:"";position:absolute;left:50%;bottom:0;width:0;height:2px;background:black;transition:.3s}
.nav-links a:hover::after{width:100%;left:0}
.nav-search{display:flex;align-items:center;background:#fdf8f2;border-radius:25px;padding:3px 13px;box-shadow:0 2px 5px rgba(0,0,0,.1)}
.nav-search input{background:transparent;border:none;font-size:10px;color:#666;flex:1;outline:none}
.nav-user{display:flex;align-items:center;gap:10px}
.nav-user a{color:black;text-decoration:none;font-size:14px}
.nav-user a:hover{color:#ff6600}
.logout-btn{border:none;background:transparent;color:#ff6600;font-size:14px;cursor:pointer}
.logout-btn:hover{text-decoration:underline}
</style>
