<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">Login</h2>
      <p class="desc">Welcome back! Please log in to continue.</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Enter your email"
          required
        />

        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter your password"
          required
        />

        <button type="submit" class="login-btn">Login</button>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      </form>

      <div class="signup-redirect">
        <p>Don't have an account?</p>
        <router-link to="/register" class="signup-link">Sign up here</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useUserStore } from "@/store/index"; 

const router = useRouter();
const userStore = useUserStore();

const email = ref("");
const password = ref("");
const errorMsg = ref("");

async function handleLogin() {
  errorMsg.value = "";
  if (!email.value || !password.value) {
    errorMsg.value = "Please fill in email and password.";
    return;
  }

  try {
    const { data } = await axios.post("/api/login", {
      email: email.value.trim(),
      password: password.value,
    });

    /* ➜ Assume that the backend returns { token, user:{ id, name, email } } */
    //localStorage.setItem("token", data.token);
    axios.defaults.headers.common["Authorization"] = `Bearer ${data.token}`;
    userStore.login(data.user, data.token);  

    router.push("/my-center");
  } catch (err) {
    errorMsg.value =
      err.response?.data?.message || "Login failed. Please try again.";
  }
}
</script>

<style scoped>
.login-container{display:flex;justify-content:center;align-items:center;background:#fffbf2;height:100vh}
.login-box{background:#fff;border-radius:8px;padding:2rem 2.5rem;box-shadow:0 4px 10px rgba(0,0,0,.1);max-width:360px;width:100%}
.login-title{text-align:center;color:#a8412a;margin-bottom:.5rem;font-size:1.8rem}
.desc{text-align:center;margin-bottom:1.5rem;color:#666}
.login-form{display:flex;flex-direction:column}
label{margin-top:.8rem;margin-bottom:.3rem;font-weight:500;color:#333}
input{padding:.5rem;font-size:.95rem;border-radius:4px;border:1px solid #ccc}
.login-btn{margin-top:1.2rem;background:#f05d37;color:#fff;padding:.6rem 1rem;border:none;border-radius:4px;cursor:pointer;font-size:1rem}
.login-btn:hover{background:#d35445}
.error{color:#e74c3c;margin-top:.6rem;text-align:center;font-size:.9rem}
.signup-redirect{text-align:center;margin-top:1rem;font-size:.95rem}
.signup-link{margin-left:5px;color:#a8412a;font-weight:500}
.signup-link:hover{color:#d35445}
</style>

  
