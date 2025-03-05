<template>
    <div class="novel-list">
      <NovelCard v-for="novel in novels" :key="novel.id" :novel="novel" />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import NovelCard from './NovelCard.vue';
  
  const novels = ref([
    { id: 1, title: "The Great Adventure", author: "John Doe", cover: "/assets/cover1.jpg" },
    { id: 2, title: "Mystery of the Lost City", author: "Jane Smith", cover: "/assets/cover2.jpg" }
  ]);
  </script>
  
  <style scoped>
  .novel-list {
    display: flex;
    gap: 20px;
  }
  </style>