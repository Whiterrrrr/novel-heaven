<template>
    <div class="home">
      <!-- heading navigation -->
      <header class="header">
        <h1>Novel Heaven</h1>
        <input v-model="searchQuery" placeholder="Search novels..." />
        <button @click="searchNovels">Search</button>
      </header>
  
      <!-- picture-->
      <div class="carousel">
        <div v-for="novel in featuredNovels" :key="novel.id" class="carousel-item">
          <img :src="novel.image" :alt="novel.title" />
          <p>{{ novel.title }}</p>
        </div>
      </div>
  
      <!-- category navigation -->
      <nav class="categories">
        <button v-for="category in categories" :key="category" @click="filterByCategory(category)">
          {{ category }}
        </button>
      </nav>
  
      <!-- novel list -->
      <section class="novel-list">
        <h2>Popular Novels</h2>
        <div class="novel-grid">
          <NovelCard v-for="novel in filteredNovels" :key="novel.id" :novel="novel" />
        </div>
      </section>
  
      <!--ranking-->>
      <section class="ranking">
        <h2>Top Ranked Novels</h2>
        <ol>
          <li v-for="(novel, index) in rankedNovels" :key="novel.id">
            <router-link :to="'/novel/' + novel.id">
              {{ index + 1 }}. {{ novel.title }}
            </router-link>
          </li>
        </ol>
      </section>
    </div>
  </template>
  
  <script>
  import { ref, computed } from "vue";
  import NovelCard from "@/components/NovelCard.vue";
  
  export default {
    components: { NovelCard },
    setup() {
      // recommendation
      const featuredNovels = ref([
        { id: 1, title: "Martial World", image: "/assets/martial-world.jpg" },
        { id: 2, title: "Rebirth of the Rich", image: "/assets/rebirth.jpg" },
        { id: 3, title: "Supreme Magus", image: "/assets/supreme-magus.jpg" },
      ]);
  
      // category
      const categories = ref(["Fantasy", "Romance", "Sci-Fi", "Adventure", "Horror"]);
  
      // novel data
      const novels = ref([
        { id: 1, title: "Martial World", category: "Fantasy" },
        { id: 2, title: "Rebirth of the Rich", category: "Romance" },
        { id: 3, title: "Supreme Magus", category: "Sci-Fi" },
        { id: 4, title: "The Great Thief", category: "Adventure" },
        { id: 5, title: "Ghost Walker", category: "Horror" },
      ]);
  
      // ranking
      const rankedNovels = computed(() => [...novels.value].sort(() => Math.random() - 0.5).slice(0, 5));
  
      // searching function
      const searchQuery = ref("");
      const searchNovels = () => {
        console.log("Searching for:", searchQuery.value);
        // 这里可以添加 API 调用
      };
  
      // catogory sorting
      const selectedCategory = ref(null);
      const filterByCategory = (category) => {
        selectedCategory.value = category;
      };
      const filteredNovels = computed(() =>
        selectedCategory.value ? novels.value.filter((n) => n.category === selectedCategory.value) : novels.value
      );
  
      return { featuredNovels, categories, novels, rankedNovels, searchQuery, searchNovels, filterByCategory, filteredNovels };
    },
  };
  </script>
  
  <style scoped>
  /* configuration */
  .home {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
  }
  
  /* heading navigation */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #333;
    color: white;
    padding: 15px;
    border-radius: 5px;
  }
  .header input {
    padding: 8px;
    width: 200px;
  }
  .header button {
    background: #007bff;
    color: white;
    border: none;
    padding: 8px 15px;
    cursor: pointer;
  }
  
  /* picture */
  .carousel {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    margin: 20px 0;
  }
  .carousel-item {
    flex: 0 0 auto;
    width: 200px;
    text-align: center;
  }
  .carousel-item img {
    width: 100%;
    border-radius: 5px;
  }
  
  /* catogory navigation */
  .categories {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  .categories button {
    padding: 10px;
    border: none;
    background: #007bff;
    color: white;
    cursor: pointer;
  }
  
  /*novellist*/
  .novel-list {
    margin-bottom: 20px;
  }
  .novel-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }
  
  /*ranking*/
  .ranking {
    background: #f8f8f8;
    padding: 15px;
    border-radius: 5px;
  }
  .ranking ol {
    padding-left: 20px;
  }
  .ranking a {
    text-decoration: none;
    color: #007bff;
  }
  </style>
  