<template>
  <div class="home-container">
   <Carousel/>
   <RankingCarousel
      :books="books"
      @view="onViewBook"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Carousel from '../components/Carousel.vue';
import RankingCarousel from '../components/RankingCarousel.vue'
import axios from 'axios'
const router = useRouter()
const books = ref([])

/**
 * Fetches the list of hot novels from the server and updates the `books` ref.
 *
 * - Calls GET /api/novel/hot
 * - Maps each item to an object with id, title, category, and cover URL
 * - On failure, logs an error to the console
 */
async function fetchHotBooks() {
  try {
    const { data } = await axios.get('/api/novel/hot')
    books.value = data.map(item =>({
      id: item.id,
      title: item.title,
      category: item.category,
      cover: item.cover_url
      ? `/api/novel/cover/${item.cover_url}`
      : '/assets/default-cover.jpg' ,
    }))
  } catch (error) {
    console.error('Failed to fetch hot novels:', error)
  }
}

onMounted(() => {
  fetchHotBooks()
})
/**
 * Navigate to the selected book’s detail page.
 *
 * @param {Object} book - The book object.
 * @param {number|string} book.id - The ID of the book to view.
 */
const onViewBook = (book) => {
  router.push({ name: 'BookDetail', params: { id: book.id } })
}

</script>
<style scoped>

</style>
  