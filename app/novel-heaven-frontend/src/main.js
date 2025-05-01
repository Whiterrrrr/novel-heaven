import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import './assets/styles.css';

import axios from 'axios';
import { useUserStore } from '@/store/index';

/* ========= Vue / Pinia ========= */
const app   = createApp(App);
const pinia = createPinia();
app.use(pinia).use(router).mount('#app');

/* ========= Axios 默认基址 ========= */
axios.defaults.baseURL = 'https://api.novel-heaven.com'; // 按需修改

/* ========= 登录状态恢复 ========= */
const userStore = useUserStore();
userStore.initAuth();

/* ========= 开发环境 Mock ========= */
if (import.meta.env.DEV) {
  // 只有在 "npm run dev" 时才动态加载依赖
  import('axios-mock-adapter')
    .then(({ default: MockAdapter }) => {
      /* ——— 延迟 500ms 的 axios-mock-adapter ——— */
      const mock = new MockAdapter(axios, { delayResponse: 500 });

      /* ——— 你的假数据区（保持完全原样） ——— */
      const bookViewMock = {
        id: 123,
        title: '惜花芷',
        author: '空留',
        category: '宫斗',
        updateTime: '2025-04-15 11:45',
        cover: '/src/assets/covers/book1.jpeg',
        description:
          '双生妹妹嫁入皇宫前夕，遭人谋害，凌辱致死。 身为姐姐的凤九颜浴血归来，脱去一身戎装替嫁，成为一国之后。',
        likes: 10,
        likedByMe: false,
        favoritesCount: 20,
        favoritedByMe: false,
        tipsCount: 5,
        tippedByMe: false,
        myBalance: 50,
      };

      const chapterListMock = [
        { id: 1, title: '第一章 替嫁' },
        { id: 2, title: '第二章 拿惯银枪的手' },
        { id: 3, title: '第三章 掐着点回来圆房？' },
      ];

      /* 章节列表 */
      mock.onGet(/\/api\/novel\/\d+\/chapters/).reply(200, chapterListMock);
      /* 作品详情 */
      mock.onGet(/\/api\/novel\/bookview\/\d+/).reply(200, bookViewMock);

      /* 点赞 */
      mock.onPost(/\/api\/novel\/\d+\/like/).reply((cfg) => {
        const { like } = JSON.parse(cfg.data);
        bookViewMock.likedByMe = like;
        bookViewMock.likes += like ? 1 : -1;
        return [200, { success: true }];
      });

      /* 收藏 */
      mock.onPost(/\/api\/novel\/\d+\/favorite/).reply((cfg) => {
        const { favorite } = JSON.parse(cfg.data);
        bookViewMock.favoritedByMe = favorite;
        bookViewMock.favoritesCount += favorite ? 1 : -1;
        return [200, { success: true }];
      });

      /* 投币 */
      mock.onPost(/\/api\/novel\/\d+\/tip/).reply((cfg) => {
        const { tips } = JSON.parse(cfg.data);
        if (tips > bookViewMock.myBalance) {
          return [400, { message: '余额不足' }];
        }
        bookViewMock.tippedByMe = true;
        bookViewMock.tipsCount += tips;
        bookViewMock.myBalance -= tips;
        return [
          200,
          {
            tipsCount: bookViewMock.tipsCount,
            myBalance: bookViewMock.myBalance,
          },
        ];
      });

      /* 评论 */
      const commentsMock = [
        { id: 1, author: '张三', content: '这本书太精彩了！' },
        { id: 2, author: '李四', content: '文字很走心，给个👍' },
        { id: 3, author: '王五', content: '等很久了，更新加快啊～' },
      ];

      mock
        .onGet(/\/api\/novel\/\d+\/comments/)
        .reply(200, commentsMock);

      mock.onPost(/\/api\/novel\/\d+\/comments/).reply((cfg) => {
        const { content } = JSON.parse(cfg.data);
        const newCmt = {
          id: commentsMock.length + 1,
          author: '测试用户',
          content,
        };
        commentsMock.unshift(newCmt);
        return [200, newCmt];
      });
    })
    .catch(() =>
      console.warn(
        '[mock] axios-mock-adapter is not installed; skipping mock setup.'
      )
    );
}
