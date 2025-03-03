<template>
    <div>
      <h1>User Profile</h1>
      <p>Welcome, {{ user ? user.name : 'Guest' }}</p>
    </div>
  </template>
  
  <script setup>
  import { useUserStore } from '@/store';
  import { computed } from 'vue';
  
  const userStore = useUserStore();
  const user = computed(() => userStore.user);
  </script>
  