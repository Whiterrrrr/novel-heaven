<template>
  <div class="mycenter-container">
    <h1 class="center-title">My Center</h1>

    <div class="header-greeting">
      Hello, dear reader! Here is your personal space.
    </div>

    <div class="content-layout">
      <!-- Favorite Books -->
      <section class="books-section">
        <h2 class="section-title">Your Favorite Books</h2>
        <div v-if="favoriteBooks.length === 0" class="empty-placeholder">
          No favorite books yet.
        </div>
        <div class="books-grid" v-else>
          <div v-for="book in favoriteBooks" :key="book.id" class="book-item">
            <div class="cover-container">
              <img :src="book.cover" class="book-cover" alt="cover" />
            </div>
            <p class="book-title">{{ book.title }}</p>
            <p class="book-author">{{ book.author }}</p>
          </div>
        </div>
      </section>

      <!-- Right Pane -->
      <section class="right-pane">
        <!-- Author Zone -->
        <div class="author-zone">
          <h2 class="section-title">Author Zone</h2>
          <p class="zone-desc">
            Manage your creations, publish new chapters, and connect with readers.
          </p>
          <div class="author-btn-area">
            <button class="author-action-btn" @click="gotoAuthorDashboard">
              Go to Author Dashboard
            </button>
          </div>
        </div>

        <!-- Rewards -->
        <div class="rewards-section">
          <h2 class="section-title">My Rewards</h2>
          <ul v-if="rewards.length">
            <li v-for="r in rewards" :key="r.id">
              On {{ r.date }}, gave {{ r.amount }} gold coins to
              "<strong>{{ r.bookTitle }}</strong>"
            </li>
          </ul>
          <p v-else class="empty-placeholder">No rewards yet.</p>
          <p class="coin-line">My remaining coins: {{ coinBalance }}</p>
        </div>

        <!-- Comments -->
        <div class="messages-section">
          <h2 class="section-title">My Comments</h2>
          <ul v-if="comments.length">
            <li v-for="c in comments" :key="c.id">
              In "<strong>{{ c.bookTitle }}</strong>", said
              "<em>{{ c.content }}</em>" ({{ c.date }})
            </li>
          </ul>
          <p v-else class="empty-placeholder">No comments yet.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";

/* demo covers (local) */
import DouPoCover from "@/assets/斗破苍穹.jpg";
import WanMeiCover from "@/assets/完美世界.jpg";
import DaZhuZaiCover from "@/assets/大主宰.jpg";
import ZheTianCover from "@/assets/遮天.jpg";
import DouLuoCover from "@/assets/斗罗大陆.jpg";
import XingChenCover from "@/assets/星辰变.jpg";

export default {
  name: "MyCenter",
  data() {
    return {
      favoriteBooks: [],
      rewards: [],
      comments: [],
      coinBalance: 0,
      demoUsed: false, // 防止重复追加 demo
    };
  },
  created() {
    this.fetchAll();
  },
  methods: {
    gotoAuthorDashboard() {
      this.$router.push("/author-dashboard");
    },

    /* 一次并行请求，失败再落 demo */
    async fetchAll() {
      await Promise.all([
        this.fetchFavorites(),
        //this.fetchRewards(),
        //this.fetchComments(),
        //this.fetchCoins(),
      ]);

      /* 如果任何一部分仍空，统一落单次 demo */
      //if (!this.favoriteBooks.length && !this.demoUsed) {
        //this.useDemoData();
      //}
    },

    async fetchFavorites() {
      try {
        const { data } = await axios.get("/api/novel/mybookshelf");
        this.favoriteBooks = data;
      } catch {/* swallow */
        console.error('书架加载失败：', err)
      }
    },
    async fetchRewards() {
      try {
        const { data } = await axios.get("/api/user/rewards");
        this.rewards = data.records;
        this.coinBalance = data.balance;
      } catch {/* swallow */
        console.error('rewards失败：', err)
      }
    },
    async fetchComments() {
      try {
        const { data } = await axios.get("/api/user/comments");
        this.comments = data;
      } catch {/* swallow */
        console.error('comments error', err)
      }
    },
    async fetchCoins() {
      try {
        const { data } = await axios.get("/api/user/coins");
        this.coinBalance = data.balance;
      } catch {/* swallow */
        console.error('coins error', err)
      }
    },

    /* --- demo fallback --- */
    useDemoData() {
      this.demoUsed = true;

      this.favoriteBooks = [
        { id: 1, title: "Battle Through the Heavens", author: "Heavenly Silkworm Potato", cover: DouPoCover },
        { id: 2, title: "Perfect World", author: "Chen Dong", cover: WanMeiCover },
        { id: 3, title: "The Great Ruler", author: "Heavenly Silkworm Potato", cover: DaZhuZaiCover },
        { id: 4, title: "Shrouding the Heavens", author: "Chen Dong", cover: ZheTianCover },
        { id: 5, title: "Douluo Continent", author: "Tang Jia San Shao", cover: DouLuoCover },
        { id: 6, title: "Stellar Transformation", author: "I Eat Tomatoes", cover: XingChenCover },
      ];

      this.rewards = [
        { id: 1, amount: 50, bookTitle: "Martial Universe", date: "2025-04-10" },
        { id: 2, amount: 20, bookTitle: "Perfect World", date: "2025-04-12" },
      ];
      this.coinBalance = 77;

      this.comments = [
        { id: 1, bookTitle: "Wu Dong Qian Kun", content: "Update quickly!!", date: "2025-04-11" },
        { id: 2, bookTitle: "Perfect World", content: "Amazing plot!", date: "2025-04-13" },
      ];
    },
  },
};
</script>

<style scoped>
/* --- unchanged styles (identical to previous version) --- */
.mycenter-container{background:#fffaf0;min-height:100vh;padding:2rem;display:flex;flex-direction:column;font-family:"Segoe UI",sans-serif;color:#333}
.center-title{font-size:2rem;color:#a8412a;margin-bottom:1rem}
.header-greeting{display:inline-block;background:linear-gradient(to right,#fde5d3,#f8ccb9 80%);color:#a8412a;padding:.6rem 1rem;border-radius:6px;font-weight:600;box-shadow:0 1px 3px rgba(0,0,0,.1);transition:transform .3s,box-shadow .3s;margin-bottom:1.5rem}
.header-greeting:hover{transform:scale(1.02);box-shadow:0 2px 6px rgba(0,0,0,.15)}
.content-layout{display:flex;flex:1;gap:1.5rem;min-height:0}
.books-section,.right-pane{background:#fff;border-radius:8px;box-shadow:0 2px 5px rgba(0,0,0,.08);padding:1rem;overflow-y:auto}
.books-section{flex:1}
.section-title{color:#a8412a;margin-bottom:.5rem}
.empty-placeholder{color:#999}
.books-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}
.book-item{display:flex;flex-direction:column;align-items:center;background:#fffcfa;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,.08);padding:.8rem;height:220px}
.cover-container{width:80px;height:110px;margin-bottom:.5rem}
.book-cover{width:100%;height:100%;object-fit:cover;border-radius:4px}
.book-title{font-weight:600;margin:0;font-size:.9rem}
.book-author{margin:.2rem 0 0;font-size:.8rem;color:#666}
.right-pane{flex:1;display:flex;flex-direction:column;gap:1rem}
.author-zone{background:#fff;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:1rem;display:flex;flex-direction:column}
.zone-desc{color:#666;margin-bottom:.8rem}
.author-btn-area{display:flex;justify-content:center}
.author-action-btn{background:#f05d37;color:#fff;border:none;border-radius:4px;padding:.6rem 1.2rem;font-size:.9rem;cursor:pointer}
.author-action-btn:hover{background:#d35445}
.rewards-section,.messages-section{background:#fff;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:1rem;flex:1;overflow-y:auto}
.rewards-section ul,.messages-section ul{list-style:disc;padding-left:1.2rem;margin:0;color:#555}
.coin-line{margin-top:.8rem;font-weight:600;color:#a8412a}
</style>

  