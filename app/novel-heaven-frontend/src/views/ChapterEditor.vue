<template>
  <div class="chapter-editor-container">
    <div class="editor-card">
      <!-- 作品标题 -->
      <h1 class="work-title">{{ workInfo.title || 'Untitled' }}</h1>

      <!-- 状态下拉框 -->
      <div class="status-section">
        <label>Status:</label>
        <select v-model="workInfo.status" @change="updateWorkStatus">
          <option value="Ongoing">Ongoing</option>
          <option value="Finished">Finished</option>
        </select>
      </div>
      <hr />

      <!-- ===== 1. Add / Edit Chapters ===== -->
      <div class="chapter-edit-section">
        <h2>Add Chapters</h2>
        <form class="chapter-form" @submit.prevent="publishChapter">
          <label>Chapter Title (≤ 15 chars)</label>
          <input
            v-model="currentChapter.title"
            maxlength="15"
            placeholder="Enter chapter title"
          />

          <label>
            Chapter Content
            <span class="count">{{ contentCount }}/{{ maxChars }}</span>
          </label>
          <textarea
            v-model="currentChapter.content"
            :maxlength="maxChars"
            @input="updateCount"
            rows="12"
            class="content-area"
          ></textarea>

          <!-- 主按钮：Publish -->
          <button type="submit" class="save-chapter-btn">
            Publish Chapter
          </button>

          <!-- 保存草稿 -->
          <button
            type="button"
            class="draft-btn"
            @click="saveDraft"
            :disabled="!validChapter"
          >
            Save Draft
          </button>

          <!-- AI 续写 -->
          <button
            type="button"
            class="ai-btn"
            @click="continueWithAI"
            :disabled="!currentChapter.content"
          >
            AI Continued Writing
          </button>

          <p class="publish-tip">
            Once published, the chapter cannot be edited. Are you sure?
          </p>
        </form>
      </div>
      <hr />

      <!-- ===== 2. Existing Chapters ===== -->
      <div class="existing-chapters">
        <h2>Existing Chapters</h2>
        <div v-if="chapters.length === 0" class="empty-text">
          No chapters yet.
        </div>
        <div class="chapters-scroll" v-else>
          <ul>
            <li v-for="(ch, idx) in chapters" :key="idx">
              <strong>{{ ch.title }}</strong>
              <p class="chapter-snippet">{{ ch.contentSnippet }}</p>
            </li>
          </ul>
        </div>
      </div>
      <hr />

      <!-- ===== 3. Comments ===== -->
      <div class="comments-area">
        <h2>Comments</h2>
        <div class="comments-scroll">
          <ul>
            <li v-for="c in workComments" :key="c.id">
              <p>
                <strong>{{ c.user }}:</strong> {{ c.content }}
              </p>
              <small class="comment-date">{{ c.date }}</small>
            </li>
          </ul>
        </div>
      </div>

      <div class="back-area">
        <router-link to="/author-dashboard" class="back-link">
          Back to Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // CHANGE

export default {
  name: "ChapterEditor",
  props: {
    workId: { type: [String, Number], default: 0 }, // 路由 params 可传
  },
  data() {
    return {
      workInfo: { title: "Moonlit Tales", status: "Ongoing" },
      maxChars: 8000,
      contentCount: 0,
      workComments: [
        { id: 1, user: "Alice", content: "Great!", date: "2025-05-01" },
      ],
      chapters: [],
      currentChapter: { title: "", content: "" },
    };
  },
  computed: {
    validChapter() {
      return (
        this.currentChapter.title.trim() &&
        this.currentChapter.content.trim()
      );
    },
  },
  methods: {
    /* -------- 字数计数 -------- */
    updateCount() {
      this.contentCount = this.currentChapter.content.length;
    },

    /* -------- 更新作品状态 -------- */
    async updateWorkStatus() {
      try {
        await axios.put(
          `/api/author/works/${this.workId || 0}`,
          {
            /* CHANGE: 后端要求 update_content 字典 */
            update_content: { status: this.workInfo.status },
          },
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        alert("Status updated!");
      } catch {
        alert("Status update failed (offline dev mode).");
      }
    },

    /* -------- 发布章节 or 草稿工具 -------- */
    async publishChapter(isDraft = false) {
      if (!this.validChapter) {
        alert("Title & content cannot be empty");
        return;
      }

      const payload = {
        title: this.currentChapter.title,
        content: this.currentChapter.content,
        status: this.workInfo.status, // CHANGE: 按新规范包含 status
        is_draft: isDraft, // CHANGE
      };

      try {
        await axios.post(
          `/api/author/works/${this.workId || 0}/chapters`,
          payload,
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        alert(isDraft ? "Draft saved!" : "Chapter published!");

        // 前端更新列表
        const snippet =
          this.currentChapter.content.slice(0, 40).trim() + "...";
        this.chapters.push({
          title: this.currentChapter.title + (isDraft ? " (draft)" : ""),
          contentSnippet: snippet,
        });
        this.currentChapter = { title: "", content: "" };
        this.contentCount = 0;
      } catch {
        alert("API failed (offline dev mode).");
      }
    },

    /* 保存草稿 */
    saveDraft() {
      this.publishChapter(true); // isDraft = true
    },

    /* -------- AI 续写 -------- */
    async continueWithAI() {
      try {
        const { data } = await axios.post(
          "/api/author/llm",
          {
            workTitle: this.workInfo.title,
            chapterTitle: this.currentChapter.title,
            chapterContent: this.currentChapter.content,
            operation: "expand", // CHANGE: 或 "analyze"
          },
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        this.currentChapter.content +=
          "\n\n" + (data.continuedText || "(AI response…)"); // 追加
        this.updateCount();
      } catch {
        this.currentChapter.content +=
          "\n\n(AI generated continuation... dev mock)";
        this.updateCount();
      }
    },
  },
};
</script>

<style scoped>
/* —— 之前样式保持，仅少量新按钮样式 —— */
.chapter-editor-container {
  background: #fffaf0;
  min-height: 100vh;
  padding: 3.5rem 2rem 2rem;
  display: flex;
  justify-content: center;
  font-family: "Segoe UI", sans-serif;
}

.editor-card {
  background: #fff;
  width: 820px; /* 放宽可视宽度 */
  max-width: 95%;
  padding: 1.5rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}

/* ...其余样式保持一致... */
.work-title {
  font-size: 1.6rem;
  color: #a8412a;
  margin: 0 0 0.4rem;
}

.status-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 1rem 0;
}

.chapter-edit-section h2,
.existing-chapters h2,
.comments-area h2 {
  font-size: 1.2rem;
  color: #a8412a;
  margin-bottom: 0.5rem;
}

.chapter-form {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.chapter-form input,
.content-area {
  padding: 0.6rem;
  font-size: 0.95rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.content-area {
  height: 320px;
  resize: vertical;
  overflow: auto;
}

.count {
  font-size: 0.8rem;
  color: #777;
  margin-left: 0.4rem;
}

.save-chapter-btn,
.draft-btn,
.ai-btn {
  background: #f05d37;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.6rem 1.1rem;
  font-size: 0.9rem;
  cursor: pointer;
  margin-top: 0.4rem;
}

.draft-btn {
  background: #999;
  margin-left: 0;
}

.ai-btn {
  background: #4caf50;
}

.save-chapter-btn:hover {
  background: #d35445;
}
.draft-btn:hover {
  background: #777;
}
.ai-btn:hover {
  background: #449d48;
}

.publish-tip {
  font-size: 0.8rem;
  color: #a8412a;
  margin-top: 0.3rem;
}

.chapters-scroll,
.comments-scroll {
  max-height: 200px;
  overflow: auto;
  border: 1px solid #eee;
  padding: 0.6rem;
  border-radius: 4px;
}

/* 省略其他已存在样式 (与前版相同) */
.chapter-snippet {
  margin: 0.2rem 0 0;
  font-size: 0.9rem;
  color: #666;
}

.comment-date {
  font-size: 0.8rem;
  color: #777;
}

.back-area {
  text-align: right;
  margin-top: 1.5rem;
}
.back-link {
  background: #999;
  color: #fff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
}
.back-link:hover {
  background: #777;
}
</style>
