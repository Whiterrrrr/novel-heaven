<template>
    <div class="search-page">
      <div class="search-container">
        <!-- 搜索框 -->
        <div class="search-bar">
          <input
            v-model="query"
            @input="hasSearched = false"
            @keyup.enter="doSearch"
            placeholder="请输入书名或作者名"
          />
          <button @click="doSearch">搜索</button>
        </div>
  
        <!-- 只有 hasSearched 为 true 时才显示结果区域 -->
        <div v-if="hasSearched" class="results-container">
          <div class="tabs">
            <button :class="{ active: tab==='related' }" @click="tab='related'">
              相关
            </button>
          </div>
  
          <div class="result-count">共 {{ filtered.length }} 项相关的结果</div>
  
          <div class="grid">
            <div v-for="novel in filtered" :key="novel.id" class="book-card">
              <img :src="novel.cover" class="cover" />
              <div class="info">
                <div class="title">{{ novel.title }}</div>
                <div class="author">作者：{{ novel.author }}</div>
                <div class="meta">{{ novel.status }} · {{ novel.wordCount }}万字</div>
                <div class="desc">{{ novel.description }}</div>
                <div class="update">最近更新：{{ novel.updateTime }}</div>
                <router-link
                  :to="`/novel/${novel.id}/content/1`"
                  class="read-now"
                >立即阅读</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import novels from '@/data/novels.js';
  
  const route = useRoute();
  const router = useRouter();
  
  const query = ref('');
  const hasSearched = ref(false);
  const tab = ref('related');
  

// 路由 ?q=xxx 一变就触发一次搜索（immediate: true 保证初始化也触发）
watch(
  () => route.query.q,
  (q) => {
    if (q && typeof q === 'string' && q.trim()) {
      query.value = q;
      hasSearched.value = true;
    } else {
      hasSearched.value = false;
    }
  },
  { immediate: true }
);
  
  // 点击搜索按钮
  function doSearch() {
    const q = query.value.trim();
    if (!q) {
      hasSearched.value = false;
      return;
    }
    hasSearched.value = true;
    // 把关键词推到 URL，便于刷新或分享恢复
    router.push({ path: '/search', query: { q } });
  }
  
  // “相关”标签下的过滤逻辑
  const filtered = computed(() => {
    if (!hasSearched.value) return [];
    const q = query.value.trim().toLowerCase();
    return novels.filter(
      n =>
        n.title.toLowerCase().includes(q) ||
        n.author.toLowerCase().includes(q)
    );
  });
  </script>
    