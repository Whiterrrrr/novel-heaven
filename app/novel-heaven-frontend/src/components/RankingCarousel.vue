<template>
    <div class="ranking-carousel" @mouseenter="stopAuto" @mouseleave="startAuto">
      <!-- 排行榜标题 -->
      <div class="ranking-title">
        <span class="title-decor">✨</span> Novel Ranking <span class="title-decor">✨</span>
      </div>
      <!-- 3×3 网格 -->
      <div class="grid">
        <!-- 使用 NovelCard 组件来显示每本小说 -->
        <NovelCard
        v-for="(book, i) in currentBatch"
        :key="book.id"
        :novel="{ 
        ...book, 
        // 全局序号 = 批次索引 * 每页大小 + 当前 i + 1
       rank: String(currentIndex * batchSize + i + 1).padStart(2, '0') 
  }" 
  @click="viewDetails(book)"/>

      </div>
      <!-- 左右切换 -->
      <button class="nav prev" @click="prevBatch">‹</button>
      <button class="nav next" @click="nextBatch">›</button>
      <!-- 圆点指示 -->
      <div class="indicators">
        <span
          v-for="(_, i) in totalBatches"
          :key="i"
          :class="{ active: i === currentIndex }"
          @click="goToBatch(i)"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, onUnmounted } from 'vue';
  import NovelCard from './NovelCard.vue'; // 导入 NovelCard 组件
  
  const props = defineProps({
    books: {
      type: Array,
      required: true,
    }
  });
  
  const emit = defineEmits(['view']);
  const batchSize = 9;
  const currentIndex = ref(0);
  const totalBatches = computed(() =>
    Math.ceil(props.books.length / batchSize)
  );
  const currentBatch = computed(() =>
    props.books.slice(
      currentIndex.value * batchSize,
      (currentIndex.value + 1) * batchSize
    )
  );
  
  let timer = null;
  const startAuto = () => {
    stopAuto();
    timer = setInterval(nextBatch, 6000);
  };
  const stopAuto = () => {
    if (timer) clearInterval(timer);
  };
  const nextBatch = () => {
    currentIndex.value = (currentIndex.value + 1) % totalBatches.value;
  };
  const prevBatch = () => {
    currentIndex.value = (currentIndex.value - 1 + totalBatches.value) % totalBatches.value;
  };
  const goToBatch = (i) => {
    currentIndex.value = i;
  };
  
  const viewDetails = (book) => {
    emit('view', book);
  };
  
  onMounted(startAuto);
  onUnmounted(stopAuto);
  </script>
  
  <style scoped>
  /* 排行榜标题 */
  .ranking-title {
    font-family: "Delius", cursive;
    margin-top: -30px;
    margin-bottom: 20px;
    margin-left: 150px;
    font-size: 24px;
    font-weight: bold;
    text-align: left;
    color: #333;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .title-decor {
    font-size: 20px;
    color: #f5b900; /* 橙色装饰 */
  }
  
  .ranking-carousel {

    position: relative;
    margin: 24px 0;
    z-index: 5;
    margin-top: 400px;
  }
  
  .grid {
    margin-left: 160px;
    margin-right:160px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
  
  .nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.8);
    font-size: 1.4em;
    cursor: pointer;
  }
  
  .prev { left: 8px; }
  .next { right: 8px; }
  
  /* 圆点指示 */
  .indicators {
    text-align: center;
    margin-top: 12px;
  }
  
  .indicators span {
    display: inline-block;
    width: 8px; height: 8px;
    margin: 0 4px;
    border-radius: 50%;
    background: #ccc;
    cursor: pointer;
  }
  
  .indicators .active {
    background: #f60;
  }
  </style>
  
  
  
  
  