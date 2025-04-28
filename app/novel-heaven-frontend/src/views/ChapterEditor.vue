<template>
  <div class="chapter-editor-container">
    <div class="editor-card">
      <!-- Work title & status -->
      <h1 class="work-title">{{ workInfo.title || "Untitled" }}</h1>
      <div class="status-section">
        <label>Status:</label>
        <select v-model="workInfo.status" @change="updateWorkStatus">
          <option value="Ongoing">Ongoing</option>
          <option value="Finished">Finished</option>
        </select>
      </div>
      <hr />

      <!-- 1. Add Chapters -->
      <div class="chapter-edit-section">
        <h2>Add Chapters</h2>

        <form class="chapter-form" @submit.prevent="publishChapter">
          <!-- Chapter Title -->
          <label>Chapter Title (≤ 15 chars)</label>
          <input
            v-model="currentChapter.title"
            maxlength="15"
            placeholder="Enter chapter title"
            class="title-input"
          />

          <!-- Chapter Content -->
          <label>
            Chapter Content
            <span class="count">{{ contentCount }}/{{ maxChars }}</span>
          </label>
          <textarea
            v-model="currentChapter.content"
            class="content-area"
            :maxlength="maxChars"
            @input="updateCount"
          ></textarea>

          <!-- Buttons -->
          <div class="button-group">
            <button type="submit" class="primary-btn">Publish Chapter</button>
            <button type="button" class="secondary-btn" @click="saveDraft">
              Save Draft
            </button>
            <button type="button" class="ai-btn" @click="continueWithAI">
              AI Continued Writing
            </button>
          </div>

          <p class="publish-tip">
            Once published, the chapter cannot be edited. Are you sure?
          </p>
        </form>
      </div>
      <hr />

      <!-- 2. Existing Chapters -->
      <div class="existing-chapters">
        <h2>Existing Chapters</h2>
        <p v-if="chapters.length === 0" class="empty-text">No chapters yet.</p>
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

      <!-- 3. Comments -->
      <div class="comments-area">
        <h2>Comments</h2>
        <div class="comments-scroll">
          <ul>
            <li v-for="(c, index) in workComments" :key="index">
              <p><strong>{{ c.user }}:</strong> {{ c.content }}</p>
              <small class="comment-date">{{ c.date }}</small>
            </li>
          </ul>
        </div>
      </div>

      <!-- Back -->
      <div class="back-area">
        <router-link to="/author-dashboard" class="back-link">
          Back to Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChapterEditor",
  data() {
    return {
      workId: this.$route.params.workId || 0,
      workInfo: { title: "Moonlit Tales", status: "Ongoing" },
      maxChars: 8000,
      contentCount: 0,

      /* demo comments */
      workComments: [
        { user: "Alice", content: "非常喜欢你的文风！", date: "2025-05-01" },
        { user: "Bob", content: "期待下一章更新～", date: "2025-05-02" },
      ],

      /* demo chapters */
      chapters: [
        { title: "Prologue", contentSnippet: "In a silent night under the moon..." },
      ],

      currentChapter: { title: "", content: "" },
    };
  },

  methods: {
    updateWorkStatus() {
      /* send to backend */
      axios.put(`/api/author/works/${this.workId}/status`, { status: this.workInfo.status })
           .catch(() => console.warn("Status update simulated in dev."));
    },

    updateCount() {
      this.contentCount = this.currentChapter.content.length;
    },

    async publishChapter() {
      if (!this.validateChapter()) return;

      const payload = { ...this.currentChapter };
      let success = false;
      try {
        await axios.post(`/api/author/works/${this.workId}/chapters`, payload);
        success = true;
      } catch {
        console.warn("Publish API failed – using local add (dev mode)");
      }
      if (!success && location.hostname !== "localhost") return;

      this.addToLocal("published");
      alert("Chapter published!");
    },

    async saveDraft() {
      if (!this.validateChapter()) return;

      const payload = { ...this.currentChapter };
      let success = false;
      try {
        await axios.post(`/api/author/works/${this.workId}/drafts`, payload);
        success = true;
      } catch {
        console.warn("Save draft API failed – using local add (dev mode)");
      }
      if (!success && location.hostname !== "localhost") return;

      this.addToLocal("draft");
      alert("Draft saved!");
    },

    async continueWithAI() {
      if (!this.currentChapter.content.trim()) {
        return alert("Please write some content first.");
      }

      try {
        const { data } = await axios.post("/api/llm/continue", {
          workTitle: this.workInfo.title,
          chapterTitle: this.currentChapter.title,
          chapterContent: this.currentChapter.content,
        });
        this.currentChapter.content += "\n\n" + data.continuedText;
        this.updateCount();
      } catch {
        console.warn("AI API failed – demo text appended.");
        /* fallback demo text */
        this.currentChapter.content += "\n\n( AI generated continuation... )";
        this.updateCount();
      }
    },

    validateChapter() {
      if (!this.currentChapter.title || !this.currentChapter.content) {
        alert("Chapter title and content cannot be empty.");
        return false;
      }
      if (this.currentChapter.title.length > 15) {
        alert("Chapter title must be 15 characters or fewer!");
        return false;
      }
      return true;
    },

    addToLocal(tag) {
      const snippet = this.currentChapter.content.slice(0, 40).trim() + "...";
      this.chapters.push({
        title: `${this.currentChapter.title} (${tag})`,
        contentSnippet: snippet,
      });
      this.currentChapter = { title: "", content: "" };
      this.contentCount = 0;
    },
  },
};
</script>

<style scoped>
/* 宽度 1100px */
.chapter-editor-container {
  background: #fffaf0;
  min-height: 100vh;
  padding: 3rem 2rem;
  display: flex;
  justify-content: center;
  font-family: "Segoe UI", sans-serif;
}
.editor-card {
  background: #fff;
  width: 1100px;
  max-width: 98%;
  padding: 2.2rem 2.8rem;
  border-radius: 10px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

/* 标题与状态 */
.work-title { font-size: 1.9rem; color: #a8412a; margin: 0 0 .7rem; }
.status-section { display: flex; gap: .7rem; margin-bottom: 1rem; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.3rem 0; }

/* 输入美化 */
.title-input,
.content-area {
  width: 100%;
  padding: .9rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  transition: border-color .2s, box-shadow .2s;
}
.title-input:focus,
.content-area:focus {
  outline: none;
  border-color: #a8412a;
  box-shadow: 0 0 4px rgba(168, 65, 42, 0.4);
}
/* Content textarea 更大 */
.content-area { height: 480px; resize: vertical; overflow: auto; }

/*计数*/
.count { font-size: .8rem; color: #777; margin-left: .4rem; }

/* 按钮组居中 */
.button-group { display: flex; justify-content: center; gap: 1.4rem; margin-top: 1.1rem; }
.primary-btn, .secondary-btn, .ai-btn {
  border: none;
  padding: .9rem 1.8rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.primary-btn { background: #f05d37; color: #fff; }
.primary-btn:hover { background: #d35445; }
.secondary-btn { background: #666; color: #fff; }
.secondary-btn:hover { background: #555; }
.ai-btn { background: #3498db; color: #fff; }
.ai-btn:hover { background: #2980b9; }
.publish-tip { font-size: .8rem; color: #a8412a; margin-top: .4rem; }

/* Existing & Comments 区 */
.chapters-scroll, .comments-scroll {
  max-height: 240px;
  overflow: auto;
  border: 1px solid #eee;
  padding: .8rem;
  border-radius: 4px;
}
.chapter-snippet { margin: .2rem 0 0; font-size: .9rem; color: #666; }

.comments-scroll ul { list-style: none; margin: 0; padding: 0; }
.comments-scroll li { background: #fffcf5; margin: .4rem 0; padding: .5rem; border-radius: 4px; }
.comment-date { font-size: .8rem; color: #777; }

/* Back */
.back-area { text-align: right; margin-top: 1.6rem; }
.back-link {
  background: #999; color: #fff; text-decoration: none;
  padding: .6rem 1.2rem; border-radius: 4px; font-size: .9rem;
}
.back-link:hover { background: #777; }
</style>
