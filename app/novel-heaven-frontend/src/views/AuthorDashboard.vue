<template>
  <div class="author-dashboard-container">
    <!-- ======= 标题 ======= -->
    <h1 class="dashboard-title">Author Dashboard</h1>

    <!-- ======= 作者名 + 余额 ======= -->
    <div class="author-name-section">
      <span class="author-name-label">Author Name:</span>

      <!-- 若已确认则显示不可编辑文本；否则显示输入框 + 保存 -->
      <template v-if="authorNameConfirmed">
        <span class="author-name-text">{{ authorName }}</span>
      </template>
      <template v-else>
        <input
          v-model="tempName"
          maxlength="7"
          class="author-name-input"
          placeholder="Enter pen name (≤7)"
        />
        <button class="save-btn" @click="confirmAuthorName">Save</button>
      </template>

      <!-- 余额 -->
      <span class="coin-balance">Coins: {{ coinBalance }}</span>
    </div>

    <!-- ======= 我的作品 ======= -->
    <div class="my-works-section">
      <div class="works-title-area">
        <h2 class="works-title">My Works</h2>
        <button
          class="create-work-btn"
          @click="openCreateModal"
          :disabled="!authorNameConfirmed"
        >
          Create New Work
        </button>
      </div>

      <div v-if="works.length === 0" class="no-works-hint">
        No works yet, start creating!
      </div>

      <div class="works-list">
        <div v-for="work in works" :key="work.id" class="work-card">
          <!-- 封面 -->
          <img :src="work.cover" alt="cover" class="work-cover" />

          <!-- 左列：点赞 / 评论 / 状态 -->
          <div class="work-left-stats">
            <div class="stat-item">
              <span class="like-icon">♥</span>
              <span>{{ work.likes }}</span>
            </div>
            <div class="stat-item">
              <span class="comment-icon">🗩</span>
              <span>{{ work.commentsCount }}</span>
            </div>
            <div class="stat-item">Status: {{ work.status }}</div>
          </div>

          <!-- 中列：标题 / 简介 -->
          <div class="work-center">
            <h3 class="work-title">{{ work.title }}</h3>
            <p class="work-synopsis">{{ work.synopsis }}</p>
          </div>

          <!-- 右列：编辑按钮 -->
          <button
            class="edit-chapter-btn"
            @click="editChapters(work.id)"
            :disabled="!authorNameConfirmed"
          >
            Edit Chapters
          </button>
        </div>
      </div>
    </div>

    <!-- ======= 最新评论 ======= -->
    <div class="comments-section">
      <h2 class="comments-title">Latest Comments</h2>
      <div class="comments-scroll">
        <ul>
          <li v-for="c in latestComments" :key="c.id">
            <strong>{{ c.reader }}:</strong> {{ c.content }}
            <small class="cmt-date">({{ c.date }})</small>
          </li>
        </ul>
      </div>
    </div>

    <!-- ======= 新建作品弹窗 ======= -->
    <CreateWork v-model:visible="showCreateModal" @created="refreshWorks" />
  </div>
</template>

<script>
/* ---------- 依赖 ---------- */
import axios from "axios";
import CreateWork from "@/views/CreateWork.vue";
import { useUserStore } from "@/store/index";

// 假封面图片
import DouLuoCover from "@/assets/斗罗大陆.jpg";
import DouPoCover from "@/assets/斗破苍穹.jpg";
import WanMeiCover from "@/assets/完美世界.jpg";

export default {
  name: "AuthorDashboard",
  components: { CreateWork },

  data() {
    return {
      /* —— 作者名相关 —— */
      authorName: "",
      authorNameConfirmed: false,
      tempName: "",

      /* —— 账户余额 —— */
      coinBalance: 0,

      /* —— 作品列表 —— */
      works: [
        {
          id: 101,
          title: "斗罗大陆",
          cover: DouLuoCover,
          synopsis: "唐三的异世之旅，宗门崛起的故事。",
          status: "Ongoing",
          likes: 520,
          commentsCount: 88,
        },
        {
          id: 102,
          title: "斗破苍穹",
          cover: DouPoCover,
          synopsis: "萧炎三十级斗者一朝变废？却机缘巧合重登巅峰！",
          status: "Ongoing",
          likes: 888,
          commentsCount: 120,
        },
        {
          id: 103,
          title: "完美世界",
          cover: WanMeiCover,
          synopsis: "石昊于蛮荒中崛起，追寻那传说中的完美之路。",
          status: "Finished",
          likes: 666,
          commentsCount: 95,
        },
      ],

      /* —— 最新评论 —— */
      latestComments: [
        /* CHANGE: 示例评论，可由后端覆盖 */
        {
          id: 1,
          reader: "Alice",
          content: "I really like your work!",
          date: "2025-05-01",
        },
        {
          id: 2,
          reader: "Bob",
          content: "Looking forward to the next chapter!",
          date: "2025-05-02",
        },
      ],

      /* —— 弹窗开关 —— */
      showCreateModal: false,
    };
  },

  created() {
    this.initAuthorInfo(); // CHANGE
    this.refreshWorks();
    this.fetchLatestComments(); // CHANGE
  },

  methods: {
    /* ---------- 初始化作者信息 ---------- */
    async initAuthorInfo() {
      try {
        const { data } = await axios.get("/api/author/me");
        this.authorName = data.authorName;
        this.authorNameConfirmed = !!data.authorName;
        this.coinBalance = data.coins ?? 0;
        this.tempName = data.authorName;
      } catch (e) {
        /* 如后端尚未实现，用本地存储兜底 */
        const localName = localStorage.getItem("authorName");
        this.authorName = localName || "";
        this.authorNameConfirmed = !!localName;
        this.tempName = localName;
        this.coinBalance =
          parseInt(localStorage.getItem("coinBalance") || "50", 10); // 默认50
      }
    },

    /* ---------- 保存笔名 ---------- */
    async confirmAuthorName() {
      if (!this.tempName.trim()) {
        alert("Pen name cannot be empty");
        return;
      }
      try {
        await axios.post("/api/author/name", {
          authorName: this.tempName.trim(),
        });
        this.authorName = this.tempName.trim();
        this.authorNameConfirmed = true;
      } catch {
        /* 本地兜底 */
        this.authorName = this.tempName.trim();
        this.authorNameConfirmed = true;
        localStorage.setItem("authorName", this.authorName); // CHANGE
      }
    },

    /* ---------- 进入章节编辑 ---------- */
    editChapters(workId) {
      this.$router.push({ name: "ChapterEditor", params: { workId } });
    },

    /* ---------- 打开弹窗 ---------- */
    openCreateModal() {
      this.showCreateModal = true;
    },

    /* ---------- 刷新作品列表 ---------- */
    async refreshWorks() {
      try {
        const { data } = await axios.get("/api/author/works");
        this.works = data;
      } catch (err) {
        // 使用默认假数据（保持现状）
      }
    },

    /* ---------- 获取最新评论 ---------- */
    async fetchLatestComments() {
      try {
        const { data } = await axios.get("/api/author/comments?limit=10");
        this.latestComments = data;
      } catch {
        /* 若接口还没实现，保持示例 */
      }
    },
  },
};
</script>

<style scoped>
/* —— 原有样式保持不变，仅加几个新选择器 —— */
.author-dashboard-container {
  background: #fffaf0;
  min-height: 100vh;
  padding: 3rem 2rem;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
}

.dashboard-title {
  text-align: center;
  font-size: 2rem;
  color: #a8412a;
  margin-bottom: 1.5rem;
}

/* ---------- 作者名 + 余额 ---------- */
.author-name-section {
  text-align: center;
  margin-bottom: 1.5rem;
}

.author-name-label {
  font-size: 1.2rem;
  color: #a8412a;
  margin-right: 0.5rem;
}

.author-name-text {
  font-size: 1.2rem;
  font-weight: 600;
}

.author-name-input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  min-width: 180px;
}

.save-btn {
  margin-left: 0.5rem;
  background: #f05d37;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 0.8rem;
  cursor: pointer;
}

.save-btn:hover {
  background: #d35445;
}

.coin-balance {
  display: inline-block;
  margin-left: 1rem;
  color: #333;
}

/* ---------- 作品区 ---------- */
.my-works-section {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  padding: 1rem;
  overflow-y: auto;
}

.works-title-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.works-title {
  margin: 0;
  font-size: 1.4rem;
  color: #a8412a;
}

.create-work-btn {
  background: #f05d37;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.create-work-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.create-work-btn:hover:not(:disabled) {
  background: #d35445;
}

.works-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.work-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #fffcfa;
  border-radius: 6px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.work-cover {
  width: 100px;
  height: 130px;
  object-fit: cover;
  border-radius: 4px;
}

/* stats column */
.work-left-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 80px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  color: #555;
}

.like-icon {
  color: #e74c3c;
  font-size: 1.1rem;
}

.comment-icon {
  font-size: 1.1rem;
}

/* center info */
.work-center {
  flex: 1;
  text-align: center;
}

.work-title {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.work-synopsis {
  margin: 0.2rem 0 0;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

/* right button */
.edit-chapter-btn {
  margin-left: auto;
  background: #f05d37;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
}

.edit-chapter-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.edit-chapter-btn:hover:not(:disabled) {
  background: #d35445;
}

/* ---------- 最新评论 ---------- */
.comments-section {
  margin-top: 1.5rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  padding: 1rem;
}

.comments-title {
  margin: 0 0 0.6rem;
  font-size: 1.3rem;
  color: #a8412a;
}

.comments-scroll {
  max-height: 180px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 0.6rem;
}

.comments-scroll ul {
  margin: 0;
  padding: 0;
  list-style: disc inside;
}

.cmt-date {
  font-size: 0.8rem;
  color: #777;
  margin-left: 0.4rem;
}
</style>
