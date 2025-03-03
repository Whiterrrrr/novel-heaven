<template>
    <div class="novel-card">
      <h3>{{ novel.title }}</h3>
      <router-link :to="'/novel/' + novel.id">Read More</router-link>
    </div>
  </template>
  
  <script setup>
  defineProps(["novel"]);
  </script>
  
  <style scoped>
  .novel-card {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    text-align: center;
  }
  .novel-card h3 {
    margin: 0;
  }
  .novel-card a {
    text-decoration: none;
    color: #007bff;
  }
  </style>