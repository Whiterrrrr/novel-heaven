<template>
  <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Delius&family=Lavishly+Yours&family=Ma+Shan+Zheng&display=swap" rel="stylesheet">
 <div class="novel-detail">
   <!-- 顶部部分：封面、标题、字数、更新日期 -->
   <div class="novel-header">
     <img :src="novel.cover" alt="cover" class="novel-cover" />
     <div class="novel-info">
       <h1 class="novel-title">{{ novel.title }}</h1>
       <div class="novel-meta">
         <span class="author">{{ novel.author }}</span>
       </div>
       <div class="read-btn-container">
         <router-link :to="'/novel/' + novel.id +'/content/1'" class="read-btn">开始阅读</router-link>
         <button @click="toggleFavorite" :class="{'favorited': isFavorited}" class="favorite-btn">
           <svg xmlns="http://www.w3.org/2000/svg" fill="none" width="24" height="24" viewBox="0 0 24 24" stroke="currentColor">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
           </svg>
         </button>
       </div>
     </div>
   </div>
 </div>
 <div class="detail-extra">
    <div class="detail-extra-container">
      <!-- 作品简介 -->
      <section class="intro-section">
        <h3>作品简介</h3>
        <hr class="section-divider" />
        <p class="intro-text">{{ novel.description }}</p>
      </section>

      <!-- 目录 -->
      <section class="toc-section">
        <h3>目录</h3>
        <hr class="section-divider" />
        <ul class="chapter-list">
          <li v-for="ch in chaptersList" :key="ch.id">
            <router-link
              :to="`/novel/${novel.id}/content/${ch.id}`"
              class="chapter-link"
            >{{ ch.title }}</router-link>
          </li>
        </ul>
      </section>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const novelId = route.params.id; 

const novel = ref({});
const isFavorited = ref(false);  // 收藏状态

onMounted(async () => {
 // 使用假数据加载小说详情（在实际应用中可以从后端获取数据）
 novel.value = {
   id: novelId,
   title: '惜花芷',
   author: '空留',
   category:"宫斗",
   updateTime: '2025-04-15 11:45',
   cover: '/src/assets/covers/book1.jpeg', 
   description: '双生妹妹嫁入皇宫前夕，遭人谋害，凌辱致死。 身为姐姐的凤九颜浴血归来，脱去一身戎装替嫁，成为一国之后。 然后，她杀疯了！ 皇帝有白月光，她出嫁时，都以为她不得圣宠。 听着那些人的嘲笑侮辱，她不屑一顾。 因为，她入宫，不为争宠，只为杀光伤害妹妹的仇人…… 报完仇，她断然离开。 皇帝却把自己洗干净了，抓着她的衣角求她，“皇后，你看，朕还能要吗？” 她一脚踹开..'
 };
});
const chaptersList = ref([
  { id: 1, title: '第一章 替嫁' },
  { id: 2, title: '第二章 拿惯银枪的手' },
  { id: 3, title: '第三章 掐着点回来圆房？' },
  // …根据实际章节数自行补充
]);


// 切换收藏状态
const toggleFavorite = () => {
 isFavorited.value = !isFavorited.value;
};
</script>

<style scoped>
.novel-detail {
 max-width: 1000px;
 padding: 20px;
 margin-top: 80px;
 margin-left: 220px;
 display: flex;
 flex-direction: row;
}

.novel-header {
 display: flex;
 flex-direction: row;
 align-items: center;
 margin-bottom: 20px;
 width: 100%;
}

.novel-cover {
 width: 180*2px;
 height: 240*2px;
 object-fit: cover;
 border-radius: 5px;
 margin-right: 30px;
}

.novel-info {
 flex: 1;
 display: flex;
 flex-direction: column;
 justify-content: flex-start;
 border-left: 2px solid #ccc;

}

.novel-title {
 font-family: "Ma Shan Zheng", cursive;
 font-size: 60px;
 font-weight: bold;
 margin-bottom: 10px;
 margin-top: 10px;
}

.novel-meta {
 font-size: 14px;
 color: #888;
}

.novel-meta span {
 margin-right: 15px;
}

.read-btn-container {
 margin-left:280px;
 margin-right: 200px;
 display: flex;
 align-items: center;
 gap: 15px;
}

.read-btn {

 display: inline-block;
 padding: 10px 55px;
 background-color: #ff6600;
 color: white;
 text-decoration: none;
 border-radius: 5px;
 font-size: 16px;
 margin-top: 20px;
 
 border: 1px solid #ff6600;
}

.read-btn:hover {
 background-color: white;
 color: #ff6600;
}

.favorite-btn {
 margin-left:10px;
 margin-top:20px;
 border: none;
 background-color: transparent;
 cursor: pointer;
}

.favorite-btn.favorited path {
 fill: red; /* 设置为红色表示已收藏 */
}

.novel-description {
 margin-top: 30px;
 font-size: 16px;
 color: #555;
}

.novel-description h3 {
 font-size: 20px;
 font-weight: bold;
}

.novel-description p {
 font-size: 16px;
 line-height: 1.5;
}



/* 响应式设计 */
@media screen and (max-width: 768px) {
 .novel-header {
   flex-direction: column;
   align-items: center;
 }

 .novel-cover {
   width: 120px;
   height: 160px;
 }

 .novel-info {
   text-align: center;
   border-left: none;
   padding-left: 0;
 }
}
/* —— 新增 “作品简介 + 目录” 区块样式 —— */
.detail-extra {
  background: #f5f5f5;
  padding: 40px 0;
}
.detail-extra-container {
  max-width: 1200px;
  margin: 0 auto;
  background: #fff;
  border-radius: 8px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* 标题 & 分界线 */
.intro-section h3,
.toc-section h3 {
  margin-left:20px;
  margin-bottom: 16px;
  text-align: left;
  font-size: 24px;
  font-weight: bold;
  
}
.section-divider {
  border: none;
  height: 1px;
  background: #e0e0e0;
}

/* 简介文本 */
.intro-text {
  margin-top:35px;
  margin-bottom:35px;
  margin-left:40px;
  text-align: left;
  font-size: 14px;
  line-height: 1.6;
  color: #555;
}

/* 目录列表 */
.chapter-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  row-gap: 12px;
  column-gap: 24px;
}
.chapter-list li {
  margin: 4px 0;
}
.chapter-link {
  text-decoration: none;
  color: #333;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: color .2s, background .2s;
}
.chapter-link:hover {
  color: #fff;
  background: #ff6600;
}

</style> 





  