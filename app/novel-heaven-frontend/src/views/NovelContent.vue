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
//chatpeter1Content,chatpeter2Content,chatpeter3Content都是为了测试布局的假数据
import { chapter1Content } from '@/data/chapterContents.js';
import { chapter2Content, chapter3Content } from '../data/chapterContents';
import axios from 'axios'

const route = useRoute();
const router = useRouter();
const novelId = route.params.id;
const chapterId = route.params.chapterId;
const novelTitle = ref('');

//假数据
onMounted(() => {
  novelTitle.value = '惜花芷';
});
//假数据
const chapters = ref([
  { id: 1, title: '第一章 替嫁', content: chapter1Content },
  { id: 2, title: '第二章 拿惯银枪的手', content: chapter2Content },
  { id: 3, title: '第三章 掐着点回来圆房？', content: chapter3Content },
  // 更多章节...
]);


 async function loadNovelMeta() {
  try {
    const { data } = await axios.get(`/api/novel/${novelId}`)
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
    const cid = chapterId.value
    const { data } = await axios.get(
      `/api/novel/${novelId}/chapters/${cid}/content`
    )
    currentChapter.value = data
  } catch (err) {
    console.error('加载章节内容失败：', err)
  }
}
// 监听页面参数变化，翻页时自动刷新正文
//watch(
//  () => route.params.chapterId,
//  newId => {
//    chapterId.value = newId
//    loadChapterContent()
//  }
//)

//测试调用函数请用这个，把上面的假数据注释掉
//onMounted(() => {
//  loadNovelMeta()
//  loadChaptersList()
//  loadChapterContent()
//})

const contentLines = computed(() =>
  currentChapter.value.content
    .split(/\r?\n/)       // 按回车拆行
    .map(l => l.trim())    // 去掉首尾空格
    .filter(l => l)        // 去掉空行
);

const currentChapter = computed(() => {
  const cid = parseInt(route.params.chapterId, 10);
  return chapters.value.find(ch => ch.id === cid) || { title: '', content: '' };
});

// 计算下一章（如果有）
const nextChapter = computed(() => {
  const cid = parseInt(route.params.chapterId, 10);
  return chapters.value.find(ch => ch.id === cid + 1) || null;
});
// 计算上一章（如果有）
const prevChapter = computed(() => {
  const cid = parseInt(route.params.chapterId, 10);
  return chapters.value.find(ch => ch.id === cid - 1) || null;
});

const isFirstChapter = computed(() => !prevChapter.value);

const isLastChapter = computed(() => {
  const cid = parseInt(route.params.chapterId, 10);
  return cid === chapters.value.length;  // 如果当前章节是最后一章，返回 true
});
// 跳转到下一章
function goToNextChapter() {
  router.push(`/novel/${novelId}/content/${nextChapter.value.id}`);
}
// 跳转到上一章
function goToPrevChapter() {
  router.push(`/novel/${novelId}/content/${prevChapter.value.id}`);
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

