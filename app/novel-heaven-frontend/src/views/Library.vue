<template>
    <div class="library">
      <!-- fliterring -->
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
  
      <!-- sorting tabs -->
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
  
      <!-- book list -->
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
            <div class="author">Author：{{ book.author }}</div>
            <div class="meta">{{ book.status }} · {{ book.wordCount }}</div>
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
  
  // sorting tabs
  const sortTabs = ['Hot', 'New'];
  const selectedSort = ref(sortTabs[0]);
  
  const books = ref([]);
  
  /**
 * Fetches up to 10 novel categories from the API and initializes the category list.
 *
 * - Calls GET /api/novel/categories?limit=10
 * - Prepends "All" to the returned categories
 * - Sets the first category as the default selection
 */
  async function fetchCategories() {
  try {
    const { data } = await axios.get('/api/novel/categories', {
      params: { limit: 10 }
    })
    categories.value = ['All', ...data.map(c => c.category)]
    selectedCategory.value = categories.value[0]
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}
/**
 * Fetches the list of novels for the selected category and updates the `books` ref.
 *
 * - If `selectedCategory` is not "All", includes `category_name` as a query param.
 * - Calls GET /api/novel/categories/list with appropriate params.
 * - Maps each returned item to an object with id, title, author, status, word count,
 *   cover URL, description, update time, category, views, and likes.
 * - On failure, logs an error to the console.
 */
async function fetchBooks() {
  try {
    const params = {}
    if (selectedCategory.value !== 'All') {
      params.category_name = selectedCategory.value
    }
    const { data } = await axios.get('/api/novel/categories/list', { params })
    books.value = data.map(item => ({
      id:           item.id,
      title:        item.article_name,
      author:       item.author,
      status:       item.status,
      wordCount:    (item.word_count),//.toFixed(1),
      cover: item.cover_url
         ? `/api/novel/cover/${item.cover_url}`
         : '/assets/default-cover.jpg' ,
      description:  item.intro,
      updateTime:   item.latest_update_time,//.slice(0, 10),
      category:     item.category,
      views   :      item.views,
      likes   :      item.likes,
    }))
  } catch (err) {
    console.error('Failed to book list:', err)
  }
}
 
onMounted(async () => {
  await fetchCategories()
  await fetchBooks()
})  
// Re-fetch the book list whenever the selected category changes
watch(selectedCategory, fetchBooks)
// Compute a filtered list of books
  const filteredBooks = computed(() =>
  books.value.filter(b => 
    selectedCategory.value === 'All' || b.category === selectedCategory.value
  )
)
/**
 * Returns the book list sorted by a hotness score (0.7 × views + 0.3 × likes)
 * when "Hot" is selected; otherwise returns the unmodified list.
 */
const sortedBooks = computed(() => {
  if (selectedSort.value === 'Hot') {
    return [...filteredBooks.value].sort((a, b) => {
      const scoreA = a.views * 0.7 + a.likes * 0.3
      const scoreB = b.views * 0.7 + b.likes * 0.3
      return scoreB - scoreA
    })
  }
  return filteredBooks.value
})
  </script>
  
  <style scoped>
  .library {
    margin-top: 80px;
    margin-left: 100px;
    max-width: 1200px;
    padding: 20px;
  }
  
  /* fliterring row */
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
  
  /* sorting tabs */
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
  
  /* book grid */
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
  
  /* novel card */
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
   display: -webkit-box;          
   -webkit-box-orient: vertical;
   -webkit-line-clamp:1;         
   overflow: hidden;
  }
  </style>
  
  