import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import './assets/styles.css';
import axios from 'axios';
import { useUserStore } from "@/store/index";
import MockAdapter from 'axios-mock-adapter'

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount('#app');
const userStore = useUserStore();
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  userStore.setToken(token);    // 视你的 store 而定：把 token 存到 Pinia/Vuex
}

// delayResponse: 500ms 模拟网络延迟
const mock = new MockAdapter(axios, { delayResponse: 500 })

// 假数据
const bookViewMock = {
  id: 123,
   title: '惜花芷',
 author: '空留',
   category:"宫斗",
  updateTime: '2025-04-15 11:45',
   cover: '/src/assets/covers/book1.jpeg', 
   description: '双生妹妹嫁入皇宫前夕，遭人谋害，凌辱致死。 身为姐姐的凤九颜浴血归来，脱去一身戎装替嫁，成为一国之后。',
  likes:     10,
  likedByMe: false,
  favoritesCount: 20,
  favoritedByMe: false,
  tipsCount: 5,
  tippedByMe: false,
  myBalance: 50
}
// 假数据：章节列表
const chapterListMock = [
  { id: 1, title: '第一章 替嫁' },
  { id: 2, title: '第二章 拿惯银枪的手' },
  { id: 3, title: '第三章 掐着点回来圆房？' },
  // …可以随意再加
]

// 拦截 GET /api/novel/:id/chapters
mock.onGet(/\/api\/novel\/\d+\/chapters/).reply(200, chapterListMock)
// GET 小说详情
mock.onGet(/\/api\/novel\/bookview\/\d+/).reply(200, bookViewMock)

// POST 点赞
mock.onPost(/\/api\/novel\/\d+\/like/).reply(config => {
  const { like } = JSON.parse(config.data)
  // 这里可以动态修改 bookViewMock.likes/bookViewMock.likedByMe
  bookViewMock.likedByMe = like
  bookViewMock.likes += like ? +1 : -1
  return [200, { success: true }]
})

// POST 收藏
mock.onPost(/\/api\/novel\/\d+\/favorite/).reply(config => {
  const { favorite } = JSON.parse(config.data)
  bookViewMock.favoritedByMe = favorite
  bookViewMock.favoritesCount += favorite ? +1 : -1
  return [200, { success: true }]
})

// POST 投币
mock.onPost(/\/api\/novel\/\d+\/tip/).reply(config => {
  const { tips } = JSON.parse(config.data)
  if (tips > bookViewMock.myBalance) {
    return [400, { message: '余额不足' }]
  }
  bookViewMock.tippedByMe = true
  bookViewMock.tipsCount += tips
  bookViewMock.myBalance -= tips
  return [200, {
    tipsCount:    bookViewMock.tipsCount,
    myBalance:    bookViewMock.myBalance
  }]
})
const commentsMock = [
  { id: 1, author: '张三', content: '这本书太精彩了！' },
  { id: 2, author: '李四', content: '文字很走心，给个👍' },
  { id: 3, author: '王五', content: '等很久了，更新加快啊～' },
]

// GET 章节评论列表
mock.onGet(/\/api\/novel\/\d+\/comments/).reply(200, commentsMock)

// POST 提交新评论
mock.onPost(/\/api\/novel\/\d+\/comments/).reply(config => {
  const { content } = JSON.parse(config.data)
  // 这里 author 可以写死为当前登录用户
  const newCmt = {
    id: commentsMock.length + 1,
    author: '测试用户',
    content
  }
  // 新评论插到数组头
  commentsMock.unshift(newCmt)
  return [200, newCmt]
})