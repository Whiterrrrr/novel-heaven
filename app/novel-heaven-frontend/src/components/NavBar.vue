<template>
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/profile">Profile</router-link>
      <router-link to="/login">Login</router-link>
    </nav>
  </template>
  
  <style scoped>
  nav {
    display: flex;
    justify-content: space-around;
    background: #333;
    padding: 10px;
  }
  
  nav a {
    color: white;
    text-decoration: none;
  }
  </style>