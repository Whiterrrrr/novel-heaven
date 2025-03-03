<template>
    <div class="register">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <label for="username">Username:</label>
        <input v-model="username" id="username" required />
  
        <label for="email">Email:</label>
        <input v-model="email" type="email" id="email" required />
  
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" required />
  
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: "",
        email: "",
        password: "",
      };
    },
    methods: {
      register() {
        console.log("Registering:", this.username, this.email, this.password);
        
      },
    },
  };
  </script>
  
  <style scoped>
  .register {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  input {
    display: block;
    width: 100%;
    margin-bottom: 10px;
    padding: 5px;
  }
  button {
    width: 100%;
    padding: 10px;
    background: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>