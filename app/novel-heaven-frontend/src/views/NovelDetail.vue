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
            <router-link
              :to="'/novel/' + novel.id + '/content/1'"
              class="read-btn"
            >
              开始阅读
            </router-link>
            <button
              @click="handleFavoriteClick"
              :class="{ favorited: isFavorited }"
              class="favorite-btn"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 
                     2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09
                     C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5
                     c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                />
              </svg>
            </button>
            <button @click="handleCoinClick" class="coin-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" stroke="#666" stroke-width="2" fill="#FFF"/>
  <text x="12" y="16" text-anchor="middle" font-size="12" fill="#666" font-family="Arial">¥</text>
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
  <!-- —— 新增 “评论区” 外层包裹 —— -->
  <div class="comment-extra">
      <div class="comment-extra-container">
        <div class="comment-header">
          <span class="comment-count">评论</span>
        </div>
  
        <div class="comment-section">
          <div v-if="!userStore.isAuthenticated" class="login-prompt">
            <router-link to="/login">请先 登录 后发表评论 (｡･ω･｡)</router-link>
          </div>
          <div v-else class="comment-form">
            <textarea
              ref="commentTextarea"
              v-model="newComment"
              placeholder="写下你的评论..."
              rows="1"
              @input="autoResize"
            ></textarea>
            <div class="comment-form-actions">
              <button @click="submitComment">发表评论</button>
            </div>
          </div>
  
          <div class="comments-list">
            <div
              v-for="c in comments"
              :key="c.id"
              class="comment-item"
            >
              <div class="comment-author">{{ c.author }}</div>
              <div class="comment-content">{{ c.content }}</div>
            </div>
            <div v-if="comments.length === 0" class="no-comments">
              暂无评论，快来抢沙发！
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted,computed} from 'vue';
import { useRoute,useRouter } from 'vue-router';
import { useUserStore } from '@/store/index';
const route = useRoute()
const router = useRouter()
import axios from 'axios';

const novelId = route.params.id; 

const novel = ref({});
const isFavorited = ref(false);  // 收藏状态


const userStore = useUserStore();
//const comments = ref([]);
// 假数据，仅用来看排版布局
const comments = ref([
    { id: 1, author: '张三', content: '这本书太精彩了！' },
    { id: 2, author: '李四', content: '文字很走心，给个👍' },
    { id: 3, author: '王五', content: '等很久了，更新加快啊～' }
  ])
const newComment = ref('');
const commentTextarea = ref(null)

  function handleFavoriteClick() {
  if (!userStore.isAuthenticated) {
    alert('请先登录！')
    return
  }
  toggleFavorite();
}
  
  function autoResize() {
    const ta = commentTextarea.value
    if (!ta) return
    ta.style.height = 'auto'
    ta.style.height = ta.scrollHeight + 'px'
  }

async function loadNovelDetail() {
  try {
    const { data } = await axios.get(`/api/novel/${novelId}`)
    novel.value = data
  } catch (err) {
    console.error('加载小说详情失败：', err)
    // TODO: 可展示提示或使用默认占位数据
  }
}
async function loadChaptersList() {
  try {
    const { data } = await axios.get(`/api/novel/${novelId}/chapters`)
    chaptersList.value = data
  } catch (err) {
    console.error('加载章节列表失败：', err)
  }
}
async function fetchComments() {
  try {
    const { data } = await axios.get(`/api/novel/${novelId}/comments`)
    comments.value = data
  } catch (err) {
    console.error('加载评论失败：', err)
  }
}
async function submitComment() {
  const txt = newComment.value.trim()
  if (!txt) return
  try {
    await axios.post(`/api/novel/${novelId}/comments`, { content: txt })
    newComment.value = ''
    fetchComments()
  } catch (err) {
    console.error('提交评论失败：', err)
    
  }
}
async function toggleFavorite() {
  // 优先更新本地 UI 状态
  isFavorited.value = !isFavorited.value

  try {
    // 同步到后端
    await axios.post(
      `/api/novel/${novelId}/favorite`,
      { favorite: isFavorited.value }
    )
  } catch (err) {
    console.error('同步收藏状态失败：', err)
    // 回滚本地状态，保证 UI 与后端一致
    isFavorited.value = !isFavorited.value
    // 可在这里触发错误提示，比如 toast 或对话框
  }
}
async function handleCoinClick() {
  if (!userStore.isAuthenticated) {
    alert('请先登录！')
    return;
  }
  try {
    // 向后端申请扣币，接口路径可按实际修改
    await axios.post(`/api/novel/${novelId}/coin`);
    // TODO: 更新用户余额或给个成功提示
  } catch (err) {
    // 余额不足后端返回 400 时
    if (err.response?.status === 400) {
      alert('余额不足');
    } else {
      console.error('投币失败', err);
    }
  }
}

//onMounted(() => {
//  loadNovelDetail()
//  loadChaptersList()
//  fetchComments()
//})
// 假数据，仅用来看排版布局，测试通信函数使用上面那个
onMounted(async () => {
 
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
// 假数据，仅用来看排版布局
const chaptersList = ref([
  { id: 1, title: '第一章 替嫁' },
  { id: 2, title: '第二章 拿惯银枪的手' },
  { id: 3, title: '第三章 掐着点回来圆房？' },
  
]);

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
  align-items: center;   /* 新增：水平居中 */
  text-align: center;    /* 新增：文字居中 */
  

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
  margin-left:115px;
  justify-content: center;  /* 水平居中整个按钮组 */
  align-items: center;
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.read-btn {
display: inline-block;
 padding: 10px 55px;
 background-color: #ff6600;
 color: white;

 text-decoration: none;
 border-radius: 10px;
 font-size: 16px;
 margin-top: 20px;
 
 border: 1px solid #ff6600;

}

.read-btn:hover {
 background-color: white;
 color: #ff6600;
}
.favorite-btn, .coin-btn {
  margin: 0;            
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

.comment-extra {
  background: #f5f5f5;
  padding: 40px 0;
}
.comment-extra-container {
  max-width: 1200px;
  margin: 0 auto;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* 评论区头部 */
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.comment-count {
  font-size: 20px;
  font-weight: bold;
}
.comment-tabs {
  display: flex;
  align-items: center;
  font-size: 14px;
}
.comment-tabs button {
  background: none;
  border: none;
  color: #888;
  padding: 4px 8px;
  cursor: pointer;
}
.comment-tabs button.active {
  color: #333;
  font-weight: bold;
}

/* 评论表单 */
.comment-form textarea {
  font-size: 16px;      
  line-height: 1.5;
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;        /* disable manual dragging */
  overflow: hidden;
  box-sizing: border-box;
  transition: box-shadow .2s, border-color .2s;
}
.comment-form textarea:focus {
  outline: none;
  border-color: #66afe9;
  box-shadow: 0 0 2px rgba(102,175,233,0.6);
}
.comment-form-actions {
  text-align: right;
  margin-top: 8px;
}
.comment-form-actions button {
  padding: 6px 16px;
  background: #ff6600;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.comment-form-actions button:hover {
  background: #e65500;
}
/* 登录提示 */
.login-prompt {
  margin-bottom: 16px;
}
.login-prompt a {
  color: #ff6600;
  text-decoration: none;
}

/* 评论列表 */

.comment-item {
  
  max-width: 1200px; 
  padding: 12px 16px;
  margin-bottom: 12px;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.comment-author {
  margin-left:40px;
  text-align: left;
  font-weight: bold;
  font-size: 16px;
  color: #333;
  margin-bottom: 6px;
}

.comment-content {
  margin-left:40px;
  text-align: left;
  font-size: 14px;
  line-height: 1.6;
  color: #444;
}

/* 保留“暂无评论” */
.no-comments {
  text-align: center;
  color: #888;
  padding: 12px 0;
}

.coin-btn {
  margin-top: 20px;
  border: none;
  background: transparent;
  cursor: pointer;
}
.coin-btn svg {
  width: 24px;
  height: 24px;
  color: #666;
}
.coin-btn:hover svg {
  color: #ff6600;
}
</style>





  





  