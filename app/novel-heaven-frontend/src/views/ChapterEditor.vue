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
        <form class="chapter-form" @submit.prevent="publishChapter()">
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
          <button type="submit" class="save-chapter-btn" :disabled="!validChapter">
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

      <router-link to="/author-dashboard" class="back-link">
        Back to Dashboard
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChapterEditor",
  props: {
    workId: { type: [String, Number], default: 0 },
  },
  data() {
    return {
      workInfo: { title: "", status: "" },
      maxChars: 8000,
      contentCount: 0,
      workComments: [],
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
  async mounted() {
    if (this.workId) {
      this.loadWorkData();
    }
  },
  methods: {
    async loadWorkData() {
      try {
        const { data } = await axios.get(
          `/api/author/works/overview/${this.workId}`,
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        this.workInfo.title = data.title;
        this.workInfo.status = data.status;
        this.chapters = data.chapters || [];
        this.workComments = data.comments || [];
      } catch (error) {
        console.error(error);
        alert("Failed to load work data.");
      }
    },

    /* -------- 字数计数 -------- */
    updateCount() {
      this.contentCount = this.currentChapter.content.length;
    },

    /* -------- 更新作品状态 -------- */
    async updateWorkStatus() {
      try {
        await axios.put(
          `/api/author/works/${this.workId}/status`,
          { update_content: { status: this.workInfo.status } },
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
        status: this.workInfo.status,
        is_draft: isDraft,
      };

      try {
        await axios.post(
          `/api/author/works/${this.workId}/chapters`,
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
      this.publishChapter(true);
    },

    /* -------- AI 续写 -------- */
    async continueWithAI() {
      try {
        const { data } = await axios.post(
          "/api/author/llm",
          { content: this.currentChapter.content },
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        this.currentChapter.content += "\n\n" + data.continuation;
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
  margin-bottom: 1rem;
}

.status-section label {
  margin-right: 0.5rem;
}

.chapter-edit-section,
.existing-chapters,
.comments-area {
  margin-bottom: 2rem;
}

.chapter-form label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: bold;
}

.chapter-form input,
.chapter-form textarea,
.chapter-form select {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.save-chapter-btn,
.draft-btn,
.ai-btn {
  background: #e74c3c;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
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

.content-area {
  font-family: monospace;
}

.count {
  font-size: 0.9rem;
  color: #666;
}

.chapter-snippet {
  font-size: 0.9rem;
  color: #333;
}

.comments-scroll {
  max-height: 200px;
  overflow-y: auto;
}

.comment-date {
  font-size: 0.8rem;
  color: #999;
}

.empty-text {
  font-style: italic;
  color: #999;
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
