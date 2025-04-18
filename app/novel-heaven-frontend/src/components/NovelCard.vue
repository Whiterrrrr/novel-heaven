<template>
  <div class="novel-card">
    <!-- 左侧显示小说信息 -->
    <div class="card-left">
      <div class="rank">{{ novel.rank }}</div>
      <!-- 标题作为链接，悬浮变色 -->
      <router-link :to="`/novel/${novel.id}`" class="title-link">
        <h3 class="title">{{ novel.title }}</h3>
      </router-link>
      <div class="category">{{ novel.category }}</div>
    </div>
    <!-- 右侧显示封面图片 -->
    <div class="card-right">
      <img :src="novel.cover" alt="cover" class="cover" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  novel: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
.novel-card {
  display: flex;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
  transition: box-shadow 0.3s ease;
  margin: 16px 0;
}
.novel-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.card-left {
  flex: 2;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-right {
  flex: 1.5;
}

.rank {
  font-size: 1em;
  font-weight: bold;
  color: #555;
  margin-bottom: 8px;
}

.title-link {
  text-decoration: none;
  color: inherit;
}

.title {
  font-family: "Ma Shan Zheng", cursive;
  font-size: 1.2em;
  margin: 0 0 8px;
  transition: color 0.3s ease;
}

.title-link:hover .title {
  color: #ff6600;
}

.category {
  font-size: 0.85em;
  color: #888;
}

.cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>



