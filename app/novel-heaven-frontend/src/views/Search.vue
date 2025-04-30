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
  
          <div class="result-count">共 {{totalCount}} 项相关的结果</div>
  
          <div class="grid">
            <div class="pagination">
          <button
            :disabled="currentPage<=1"
            @click="changePage(currentPage-1)"
            >上一页</button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button
            :disabled="currentPage>=totalPages"
            @click="changePage(currentPage+1)"
            >下一页</button>
          </div>
            <div v-for="novel in searchResults" :key="novel.id" class="book-card">
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
  import { ref, computed, watch,onMounted} from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import axios from 'axios'
  
  const route = useRoute();
  const router = useRouter();
  
  const query = ref('');
  const hasSearched = ref(false);
  const tab = ref('related');
  const searchResults = ref([]);
  const currentPage = ref(1);
  const totalPages  = ref(1);
  const totalCount  = ref(0);
  const pageSize    = 10;

   async function searchNovels(q) {
   try {
     const { data } = await axios.get('/api/novel/search', {
       params: {
         q:         q.trim(),
         page:      currentPage.value,
         page_size: pageSize
       }
     })
     // 后端返回 { counts, items, page, total_pages }
     searchResults.value = data.items;
     totalCount.value    = data.counts;
     totalPages.value    = data.total_pages;
     currentPage.value   = data.page;
   } catch (err) {
     console.error('搜索接口调用失败：', err);
     searchResults.value = [];
     totalCount.value    = 0;
     totalPages.value    = 1;
     currentPage.value   = 1;
   }
 }


onMounted(() => {
  const q = route.query.q;
  if (typeof q === 'string' && q.trim()) {
    query.value = q;
    hasSearched.value = true;
    searchNovels(q); 
  }
});

async function doSearch() {
  const q = query.value.trim()
  if (!q) {
    hasSearched.value = false
    return
  }
  hasSearched.value = true;
  currentPage.value = 1;
  // 更新 URL
  router.push({ path: '/search', query: { q, page: currentPage.value } });
  
}

 //监听路由变化，保持页面与 URL 同步
 watch(
   () => route.query,
   async ({ q, page }) => {
     if (typeof q === 'string' && q.trim()) {
       query.value       = q;
       currentPage.value = parseInt(page) || 1;
       hasSearched.value = true;
       await searchNovels(q);
     } else {
       hasSearched.value = false;
       searchResults.value = [];
     }
   }
 )
  function changePage(p) {
  currentPage.value = p
  router.push({ path: '/search', query: { q: query.value, page: p } })
}

  </script>
  
  
  
  <style scoped>
  .search-page {
    background: #f5f5f5;
    min-height: 100vh;
    padding: 40px 0;
  }
  .search-container {
    max-width: 1000px;
    margin: 0 auto;
    margin-top:30px;
    background: #fff;
    border-radius: 8px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    min-height: 80vh
  }
  
  /* 搜索框 */
  .search-bar {
    justify-content: center;
    display: flex;
    gap: 8px;
  }
  .search-bar input {
  flex: none;
   width: 400px;

    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 25px;
    outline: none;
  }
  .search-bar button {
    padding: 8px 16px;
    background: #ff6600;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
  }
  
  /* 标签页 */
  .tabs {
    margin-top: 24px;
    display: flex;
    gap: 16px;
  }
  .tabs button {
    background: none;
    border: none;
    font-size: 16px;
    cursor: pointer;
    padding: 4px 0;
    position: relative;
  }
  .tabs button.active {
    color: #ff6600;
  }
  .tabs button.active::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0; right: 0;
    height: 2px;
    background: #ff6600;
  }
  
  /* 结果统计 */
  .result-count {
    margin: 12px 0;
    color: #666;
  }
  
  /* 一列排版 */
  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  /* 小说卡片 */
  .book-card {
    display: flex;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    overflow: hidden;
  }
  .cover {
    width: 120px;
    height: 160px;
    object-fit: cover;
  }
  .info {
    padding: 12px 16px;
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  .title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 6px;
  }
  .author, .meta, .update {
    font-size: 12px;
    color: #888;
    margin-bottom: 4px;
  }
  .desc {
    font-size: 14px;
    color: #555;
    margin: 8px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .read-now {
    margin-top: auto;
    align-self: flex-end;
    color: #ff6600;
    text-decoration: none;
    font-weight: bold;
  }
  .read-now:hover {
    text-decoration: underline;
  }
  .pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
}
.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
  </style>
  
  

  
  
  
  