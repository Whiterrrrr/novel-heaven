<template>
    <div class="library">
      <!-- 分类筛选 -->
      <div class="filter-row">
        <span class="filter-label">Category：</span>
        <button
          v-for="cat in categories"
          :key="cat"
          :class="{ active: selectedCategory === cat }"
          @click="selectedCategory = cat"
        >
          {{ cat }}
        </button>
      </div>
  
      <!-- 排序标签 -->
      <div class="sort-tabs">
        <button
          v-for="tab in sortTabs"
          :key="tab"
          :class="{ active: selectedSort === tab }"
          @click="selectedSort = tab"
        >
          {{ tab }}
        </button>
      </div>
  
      <!-- 书籍列表 -->
      <div class="grid">
        <div
          v-for="book in sortedBooks"
          :key="book.id"
          class="book-card"
        >
          <img :src="book.cover" alt="cover" class="cover" />
          <div class="info">
            <router-link :to="`/novel/${book.id}`" class="title">
            {{ book.title }}
            </router-link>
            <div class="author">作者：{{ book.author }}</div>
            <div class="meta">{{ book.status }} · {{ book.wordCount }}万字</div>
            <div class="desc">{{ book.description }}</div>
            <div class="update">{{ book.updateTime }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch} from 'vue';
  import axios from 'axios';

  const categories       = ref(['All'])
  const selectedCategory = ref('All')
  
  // 排序选项
  const sortTabs = ['Hot', 'New'];
  const selectedSort = ref(sortTabs[0]);
  
  const books = ref([]);
  
  async function fetchCategories() {
  try {
    const { data } = await axios.get('/api/novel/categories', {
      params: { limit: 10 }
    })
    // 假设后端返回 [ { id, name, usage_count }, ... ]
    categories.value = ['All', ...data.map(c => c.name)]
    // 默认选第一个
    selectedCategory.value = categories.value[0]
  } catch (err) {
    console.error('拉取分类失败', err)
  }
}
async function fetchBooks() {
  try {
    const params = {}
    if (selectedCategory.value !== 'All') {
      params.category_name = selectedCategory.value
    }
    const { data } = await axios.get('/api/novel', { params })
    // 后端 get_articles_by_category 返回 ORM 对象序列化后的字段：
    // id, article_name, status, word_count, latest_update_time, intro, author, category
    books.value = data.map(item => ({
      id:           item.id,
      title:        item.article_name,
      author:       item.author,
      status:       item.status,
      wordCount:    (item.word_count / 10000).toFixed(1),
      cover: item.cover_url
         ? `/api/novel/cover/${item.cover_url}`
         : '/assets/default-cover.jpg' ,
      description:  item.intro,
      updateTime:   item.latest_update_time.slice(0, 10),
      category:     item.category,
      views   :      item.views,
      likes   :      item.likes,
    }))
  } catch (err) {
    console.error('拉取书籍列表失败', err)
  }
}
 
onMounted(async () => {
  await fetchCategories()
  await fetchBooks()
})  

watch(selectedCategory, fetchBooks)
  // 先按分类过滤
  const filteredBooks = computed(() =>
  books.value.filter(b => 
    selectedCategory.value === 'All' || b.category === selectedCategory.value
  )
)
//只做“最热”排序，其他直接用后端默认时间顺序
const sortedBooks = computed(() => {
  // 如果选“最热”，按 views*0.7 + likes*0.3 排倒序
  if (selectedSort.value === 'Hot') {
    return [...filteredBooks.value].sort((a, b) => {
      const scoreA = a.views * 0.7 + a.likes * 0.3
      const scoreB = b.views * 0.7 + b.likes * 0.3
      return scoreB - scoreA
    })
  }
  // “最新”——后端已经按时间倒序给过来了
  return filteredBooks.value
})
function onSelectCategory(cat) {
  selectedCategory.value = cat
}
  </script>
  
  <style scoped>
  .library {
    margin-top: 80px;
    margin-left: 100px;
    max-width: 1200px;
    padding: 20px;
  }
  
  /* 分类筛选行 */
  .filter-row {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
  }
  .filter-label {
    font-weight: bold;
    margin-right: 12px;
  }
  .filter-row button {
    margin-right: 8px;
    padding: 6px 14px;
    border: 1px solid #ccc;
    background: white;
    border-radius: 16px;
    cursor: pointer;
    font-size: 14px;
  }
  .filter-row button.active {
    background: #ff6600;
    color: white;
    border-color: #ff6600;
  }
  
  /* 排序标签 */
  .sort-tabs {
    margin-top:20px;
    display: flex;
    border-bottom: 1px solid #eaeaea;
    margin-bottom: 20px;
  }
  .sort-tabs button {
    background: none;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    color: #333;
    position: relative;
  }
  .sort-tabs button.active {
    color: #ff6600;
  }
  .sort-tabs button.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: #ff6600;
  }
  
  /* 书籍网格 */
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
  
  /* 单个书籍卡片 */
  .book-card {
    display: flex;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    overflow: hidden;
    align-items:center;
  }
  .cover {
    width: 120px;
    height: 160px;
    object-fit: cover;
  }
  .info {
    padding: 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
  }
  .title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #333;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s;
}
.title:hover {
  color: #ff6600;
}
  .author, .meta, .update {
    font-size: 12px;
    color: #888;
    margin-bottom: 4px;
  }
  .desc {
    font-size: 12px;
    color: #555;
    flex: 1;
   display: -webkit-box;           /* 多行截断 */
   -webkit-box-orient: vertical;
   -webkit-line-clamp:1;          /* 限制两行 */
   overflow: hidden;
  }
  </style>
  
  