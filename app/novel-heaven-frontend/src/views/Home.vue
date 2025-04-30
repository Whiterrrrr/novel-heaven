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
const router = useRouter()
const books = ref([])

async function fetchHotBooks() {
  try {
    const { data } = await axios.get('/api/novel/hot')
    books.value = data
  } catch (error) {
    console.error('获取热门小说失败：', error)
  }
}

//onMounted(() => {
//  fetchHotBooks(27)
//})

//假数据，仅用来看排版布局，测试通信函数使用上面那个
onMounted(async () => {

  books.value = [
    {
      id: 1,
      title: '惜花芷',
      category: '宫斗',
      cover: 'src/assets/covers/book1.jpeg'  
    },
    {
      id: 2,
      title: '我不是戏神',
      category: '都市',
      cover: 'src/assets/covers/book2.jpeg'  
    },
    {
      id: 3,
      title: '斩神',
      category: '都市',
      cover: 'src/assets/covers/book3.jpeg'  
    },
    {
      id: 4,
      title: '异兽迷城',
      category: '奇幻',
      cover: 'src/assets/covers/book4.jpeg'  
    },
    {
      id: 5,
      title: '诡舍',
      category: '悬疑',
      cover: 'src/assets/covers/book5.jpeg'  
    }
  ,
    {
      id: 6,
      title: '京圈九爷',
      category: '恋爱',
      cover: 'src/assets/covers/book6.png'  
    },
    {
      id: 7,
      title: '诸神愚戏',
      category: '奇幻',
      cover: 'src/assets/covers/book7.png'  
    },
    {
      id: 8,
      title: '我，修仙大佬',
      category: '宫斗',
      cover: 'src/assets/covers/book8.png'  
    },
    {
      id: 9,
      title: '好一个乖乖女',
      category: '恋爱',
      cover: 'src/assets/covers/book9.jpeg'  
    },
    {
      id: 10,
      title: '全民求生',
      category: '都市',
      cover: 'src/assets/covers/book10.png'  
    },
   
    {
      id: 11,
      title: '天渊',
      category: '奇幻',
      cover: 'src/assets/covers/book11.jpeg'  
    },
    {
      id: 12,
      title: '摄政王',
      category: '武侠',
      cover: 'src/assets/covers/book12.png'  
    },
    {
      id: 13,
      title: '癫都癫',
      category: '恋爱',
      cover: 'src/assets/covers/book13.png'  
    },
    {
      id: 14,
      title: '洪荒',
      category: '仙侠',
      cover: 'src/assets/covers/book14.png'  
    },
    {
      id: 15,
      title: '北派盗墓',
      category: '悬疑',
      cover: 'src/assets/covers/book15.jpeg'  
    },
    {
      id: 16,
      title: '北上娇娇',
      category: '都市',
      cover: 'src/assets/covers/book16.jpeg'  
    },
    {
      id: 17,
      title: '凡骨',
      category: '仙侠',
      cover: 'src/assets/covers/book17.png'  
    },
    {
      id: 18,
      title: '夏夜有染',
      category: '都市',
      cover: 'src/assets/covers/book18.jpeg'  
    },
  ];
})


const onViewBook = (book) => {
  // 跳到详情页
  router.push({ name: 'BookDetail', params: { id: book.id } })
}

</script>
<style scoped>

</style>
  