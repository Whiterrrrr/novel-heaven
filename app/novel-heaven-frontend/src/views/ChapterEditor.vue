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

      <!-- ===== 1. Add Chapters ===== -->
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
          <button
            type="submit"
            class="save-chapter-btn"
            :disabled="!validChapter"
          >
            Publish Chapter
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
            <li v-for="(ch, idx) in chapters" :key="ch.id || idx">
              <strong>{{ ch.title }}</strong>
              <p class="chapter-snippet">{{ ch.contentSnippet }}</p>

              <!-- 修改章节按钮 -->
              <button
                type="button"
                class="save-chapter-btn"
                @click="openModifyModal(ch)"
              >
                Modify This Chapter
              </button>
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

    <!-- ===== Modify Chapter Modal ===== -->
    <div
      v-if="showModifyModal"
      class="modal-overlay"
      @click.self="closeModifyModal"
    >
      <div class="modal-content">
        <h2>Modify Chapter</h2>
        <form @submit.prevent="submitModify">
          <label>Chapter Title (≤15 chars)</label>
          <input
            v-model="modifyChapter.title"
            maxlength="15"
            required
          />

          <label>
            Chapter Content
            <span class="count">{{ modifyCount }}/{{ maxChars }}</span>
          </label>
          <textarea
            v-model="modifyChapter.content"
            :maxlength="maxChars"
            @input="updateCountModify"
            rows="12"
            class="content-area"
            required
          ></textarea>

          <button
            type="submit"
            class="save-chapter-btn"
            :disabled="!isModifyValid"
          >
            Republish Chapter
          </button>
          <button
            type="button"
            class="cancel-btn"
            @click="closeModifyModal"
          >
            Cancel
          </button>
        </form>
      </div>
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

      // —— 修改章节相关状态 —— 
      showModifyModal: false,
      modifyChapter: { id: null, title: "", content: "" },
      modifyCount: 0,
    };
  },
  computed: {
    validChapter() {
      return (
        this.currentChapter.title.trim() &&
        this.currentChapter.content.trim()
      );
    },
    isModifyValid() {
      return (
        this.modifyChapter.title.trim() &&
        this.modifyChapter.content.trim()
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
        // 假设 data.chapters 每项形如 { id, title, content }
        this.chapters = (data.chapters || []).map((ch) => ({
          ...ch,
          contentSnippet: ch.content.slice(0, 40).trim() + "...",
        }));
        this.workComments = data.comments || [];
      } catch (error) {
        console.error(error);
        alert("Failed to load work data.");
      }
    },

    /* —— 字数计数 —— */
    updateCount() {
      this.contentCount = this.currentChapter.content.length;
    },

    /* —— 更新作品状态 —— */
    async updateWorkStatus() {
      try {
        await axios.put(
          `/api/author/works/${this.workId}/status`,
          { update_content: { status: this.workInfo.status } },
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        alert("Status updated!");
      } catch {
        alert("Status update failed.");
      }
    },

    /* —— 发布章节 —— */
    async publishChapter() {
      if (!this.validChapter) {
        alert("Title & content cannot be empty");
        return;
      }
      const payload = {
        title: this.currentChapter.title,
        content: this.currentChapter.content,
        status: this.workInfo.status
      };
      try {
        await axios.post(
          `/api/author/works/${this.workId}/chapters`,
          payload,
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        alert("Chapter published!");
        this.currentChapter = { title: "", content: "" };
        this.contentCount = 0;
        this.loadWorkData();
      } catch {
        alert("Publish failed.");
      }
    },

    /* —— AI 续写 —— */
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
          "\n\n(AI generated continuation... mock)";
        this.updateCount();
      }
    },

    /* —— 打开修改模态框 —— */
    openModifyModal(ch) {
      this.modifyChapter = { ...ch };
      this.modifyCount = ch.content.length;
      this.showModifyModal = true;
    },

    /* —— 关闭修改模态框 —— */
    closeModifyModal() {
      this.showModifyModal = false;
      this.modifyChapter = { id: null, title: "", content: "" };
      this.modifyCount = 0;
    },

    /* —— 修改字数计数 —— */
    updateCountModify() {
      this.modifyCount = this.modifyChapter.content.length;
    },

    /* —— 发送修改到后端 —— */
    async submitModify() {
      if (!this.isModifyValid) return;
      try {
        await axios.put(
          `/api/author/works/${this.workId}/chapters/${this.modifyChapter.id}`,
          {
            title: this.modifyChapter.title,
            content: this.modifyChapter.content,
          },
          { headers: { Authorization: `Bearer ${localStorage.token}` } }
        );
        alert("Chapter updated!");
        this.closeModifyModal();
        this.loadWorkData();
      } catch {
        alert("Update failed.");
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
