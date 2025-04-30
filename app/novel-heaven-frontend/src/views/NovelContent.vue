<template>
  
  <div class="novel-page">
  <div class="novel-content">
         <div class="content-header">
       <router-link :to="`/novel/${novelId}`" class="back-btn">←</router-link>
       <span class="novel-name">{{ novelTitle }}</span>
     </div>
     <hr class="divider" />
    <div class="chapter">
      <h2>{{ currentChapter.title }}</h2>
      <div class="content-lines">
         <p
           v-for="(line, idx) in contentLines"
           :key="idx"
        >{{ line }}</p>
       </div>
     <div class="nav-buttons">
       <!-- 上一章 -->
       <button
         v-if="!isFirstChapter"
         @click="goToPrevChapter"
         class="prev-btn"
       >上一章</button>

       <!-- 下一章 -->
       <button
         v-if="!isLastChapter"
         @click="goToNextChapter"
         class="next-btn"
       >下一章</button>
     </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { watch } from 'vue';
import axios from 'axios'

const route = useRoute();
const router = useRouter();
const novelId = route.params.novelId;
const chapterIdxParam = computed(() => parseInt(route.params.chapterId, 10) || 1);
const novelTitle = ref('');
//const chapters = ref([]);
const chapters = ref([
  { id: 1, title: '第一章 替嫁' },
  { id: 2, title: '第二章 拿惯银枪的手' },
  { id: 3, title: '第三章 掐着点回来圆房？' },
  
]);
const currentChapter = ref({ title: '', content: '' })
const currentIndex = computed(() => chapterIdxParam.value - 1)
const isFirstChapter = computed(() => currentIndex.value <= 0)
const isLastChapter  = computed(() => currentIndex.value >= chapters.value.length - 1)

 async function loadNovelMeta() {
  try {
    const { data } = await axios.get(`/api/novel/bookview/${novelId}`)
    novelTitle.value = data.title
  } catch (err) {
    console.error('加载小说元信息失败：', err)
  }
}


async function loadChaptersList() {
  try {
    const { data } = await axios.get(`/api/novel/${novelId}/chapters`)
    chapters.value = data
  } catch (err) {
    console.error('加载章节列表失败：', err)
  }
}

async function loadChapterContent() {
  try {
    const idx = chapterIdxParam.value
    const { data } = await axios.get(
      `/api/novel/${novelId}/chapters/${idx}/content`
    )
   
    currentChapter.value = data
  } catch (err) {
    console.error('加载章节内容失败：', err)
  }
}

watch(
  () => route.params.chapterId,
  loadChapterContent,
  { immediate: true }
);

onMounted(() => {
  loadNovelMeta()
  loadChaptersList()
  loadChapterContent()
})

const contentLines = computed(() =>
  currentChapter.value.content
    .split(/\r?\n/)       // 按回车拆行
    .map(l => l.trim())    // 去掉首尾空格
    .filter(l => l)        // 去掉空行
);



// 跳转到下一章
function goToNextChapter() {
  const nextSeq = currentIndex.value + 2;  
   router.push({
    name: 'NovelContent',
     params: {
       novelId:    novelId,
       chapterId:  nextSeq
     }
  })
}
// 跳转到上一章
function goToPrevChapter() {
      const prevSeq = currentIndex.value;  
        router.push({
     name: 'NovelContent',
     params: {
       novelId:   novelId,
       chapterId: prevSeq
     }
   })
}
</script>


<style scoped>

.content-header {
  margin-left:20px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  padding-bottom: 12px;
}
.back-btn {
  font-size: 20px;
  color: #333;
  text-decoration: none;
  margin-right: 12px;
}
.novel-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}
.divider {
  border: none;
  height: 1px;
  background-color: #e0e0e0; /* 淡灰色 */
  margin: 16px 0;            /* 上下留白可根据需要调整 */
  width: 100%;  
}
 .novel-page {
   display: grid;
   grid-template-columns: 0.5fr min(1000px,80%) 0.5fr;
   background: #f5f5f5;
   min-height: 100vh;
   
 }
.novel-content {
  grid-column: 2;
  background: #fff;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.chapter {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.chapter h2 {
  font-size: 22px;
  font-weight: bold;
}

.content-lines p {
  margin-left: 20px;
  text-indent: 2em;   /* 首行缩进两格 */
  line-height: 1.6;
  text-align: left;
}
.nav-buttons {
  display: flex;
  gap: 40px;
  justify-content: center;
  margin-top: 30px;
}
.prev-btn {
  padding: 10px 40px;
  background: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 30px;
  cursor: pointer;
}
.prev-btn:hover {
  background: #e0e0e0;
}
.next-btn {
  padding: 10px 40px;
  background: #ff6600;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
}
.next-btn:hover {
  background: #e65500;
}


</style>

