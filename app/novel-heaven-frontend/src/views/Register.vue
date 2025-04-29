<template>
  <div class="register-container">
    <div class="register-box">
      <h2 class="register-title">Sign Up</h2>
      <p class="desc">Create a new account</p>

      <form @submit.prevent="handleRegister" class="register-form">
        <!-- Username -->
        <label for="username">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          placeholder="Enter your username"
          required
        />

        <!-- Email -->
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter your email"
          required
        />

        <!-- Password -->
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="10-char letters & digits"
          required
          minlength="10"
          maxlength="10"
          pattern="(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{10}"
          title="Exactly 10 characters, letters and digits mixed"
        />

        <button type="submit" class="register-btn">Sign Up</button>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      </form>

      <div class="login-redirect">
        <p>Already have an account?</p>
        <router-link to="/login" class="login-link">Go to login</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const username = ref("");
const email = ref("");
const password = ref("");
const errorMsg = ref("");

function isValidPassword(pwd) {
  /* exactly 10 chars, at least 1 letter & 1 digit */
  return /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{10}$/.test(pwd);
}

async function handleRegister() {
  errorMsg.value = "";

  /* 校验：用户名、邮箱、密码皆非空 */
  if (!username.value.trim() || !email.value.trim() || !password.value) {
    errorMsg.value = "Username, email and password are required.";
    return;
  }

  /* 密码格式检查 */
  if (!isValidPassword(password.value)) {
    errorMsg.value =
      "Password must be exactly 10 characters long and contain both letters and digits.";
    return;
  }

  try {
    await axios.post("/api/register", {
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
    });

    alert("Registration successful!");
    router.push("/login");
  } catch (err) {
    errorMsg.value =
      err.response?.data?.message || "Registration failed. Please try again.";
  }
}
</script>

<style scoped>
/* —— 样式同前 —— */
.register-container{display:flex;justify-content:center;align-items:center;background:#fffaf0;height:100vh}
.register-box{background:#fff;border-radius:8px;padding:2rem 2.5rem;box-shadow:0 4px 10px rgba(0,0,0,.1);max-width:360px;width:100%}
.register-title{text-align:center;color:#a8412a;margin-bottom:.5rem;font-size:1.8rem}
.desc{text-align:center;margin-bottom:1.5rem;color:#666}
.register-form{display:flex;flex-direction:column}
label{margin-top:.8rem;margin-bottom:.3rem;font-weight:500;color:#333}
input{padding:.5rem;font-size:.95rem;border-radius:4px;border:1px solid #ccc}
.register-btn{margin-top:1.2rem;background:#f05d37;color:#fff;padding:.6rem 1rem;border:none;border-radius:4px;cursor:pointer;font-size:1rem}
.register-btn:hover{background:#d35445}
.error{color:#e74c3c;margin-top:.6rem;text-align:center;font-size:.9rem}
.login-redirect{text-align:center;margin-top:1rem;font-size:.95rem}
.login-link{margin-left:5px;color:#a8412a;font-weight:500}
.login-link:hover{color:#d35445}
</style>
