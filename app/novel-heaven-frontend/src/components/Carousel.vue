<template>
    <div class="carousel">
        <img :src="currentImage" :key="currentIndex" class="carousel-image"
             @mouseover="pauseCarousel" 
             @mouseleave="resumeCarousel"/>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  
  // **4 张轮播图**
  const images = [
    new URL('@/assets/banner1.jpeg', import.meta.url).href,
    new URL('@/assets/banner2.jpeg', import.meta.url).href,
    new URL('@/assets/banner3.png', import.meta.url).href,
    new URL('@/assets/banner4.png', import.meta.url).href
  ];
  
  const currentIndex = ref(0);
  const currentImage = ref(images[0]);
  let interval = null;
  let timeout = null;
  
  // **自动轮播**
  const startCarousel = () => {
    interval = setInterval(() => {
      nextImage();
    }, 6000); 
  };
  
  // **切换到下一张图片**
  const nextImage = () => {
    currentIndex.value = (currentIndex.value + 1) % images.length;
    currentImage.value = images[currentIndex.value];
  };
  
  // **鼠标悬停时暂停**
  const pauseCarousel = () => {
    clearInterval(interval);
    clearTimeout(timeout);
  };
  
  // **鼠标移开 1 秒后恢复轮播**
  const resumeCarousel = () => {
    timeout = setTimeout(() => {
      startCarousel();
    }, 100);
  };
  
  // **组件挂载时启动轮播**
  onMounted(() => {
    startCarousel();
  });
  
  // **组件卸载时清除定时器**
  onUnmounted(() => {
    clearInterval(interval);
    clearTimeout(timeout);
  });
  </script>
  
  <style scoped>
  .carousel {
    width: 100%;
    height: 100px;
    overflow: hidden;
    top: 0;
    left: 0;
    z-index: 10;
  }
  
  .carousel-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    max-width: 1600px; 
    max-height: 450px;
    position: absolute;
    left: 0;
    top: 0;
  }
  

  </style>
  
  
  
  
  