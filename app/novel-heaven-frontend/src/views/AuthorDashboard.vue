<template>
  <div class="author-dashboard-container">
    <!-- Title -->
    <h1 class="dashboard-title">Author Dashboard</h1>

    <!-- ===== Author Name Section ===== -->
    <div class="author-name-wrapper">
      <template v-if="authorNameConfirmed">
        <h2 class="author-name-display">
          Author Name: <span>{{ authorName }}</span>
        </h2>
        <p class="author-name-note">
          Author name is permanent and cannot be changed.
        </p>
      </template>

      <template v-else>
        <button class="set-author-btn" @click="openAuthorDialog">
          Set Author Name
        </button>
        <p class="author-name-note">
          You must confirm an author name (≤ 7 chars) before creating works.
        </p>
      </template>
    </div>

    <!-- ===== My Works ===== -->
    <div class="my-works-section">
      <div class="works-title-area">
        <h2 class="works-title">My Works</h2>
        <button
          class="create-work-btn"
          @click="showCreateModal = true"
          :disabled="!authorNameConfirmed"
        >
          Create New Work
        </button>
      </div>

      <div v-if="works.length === 0" class="no-works-hint">
        No works yet. Start writing!
      </div>

      <div class="works-list">
        <div
          v-for="work in works"
          :key="work.id"
          class="work-card"
        >
          <!-- Cover -->
          <img :src="work.cover" alt="cover" class="work-cover" />

          <!-- Stats -->
          <div class="work-left-stats">
            <div class="stat-item">
              <span class="like-icon">♥</span><span>{{ work.likes }}</span>
            </div>
            <div class="stat-item">
              <span class="comment-icon">🗩</span><span>{{ work.commentsCount }}</span>
            </div>
            <div class="stat-item">Status: {{ work.status }}</div>
          </div>

          <!-- Center info -->
          <div class="work-center">
            <h3 class="work-title">{{ work.title }}</h3>
            <p class="work-synopsis">{{ work.synopsis }}</p>
          </div>

          <!-- Edit chapters -->
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

    <!-- ===== Create Work Modal ===== -->
    <CreateWork
      v-model:visible="showCreateModal"
      @created="refreshWorks"
    />
  </div>
</template>

<script>
import CreateWork from "@/views/CreateWork.vue";
import DouLuoCover from "@/assets/斗罗大陆.jpg";
import DouPoCover from "@/assets/斗破苍穹.jpg";
import WanMeiCover from "@/assets/完美世界.jpg";
import axios from "axios";

export default {
  name: "AuthorDashboard",
  components: { CreateWork },

  data() {
    return {
      /* Author name state */
      authorName: "",
      authorNameConfirmed: false,

      /* Works */
      works: [
        {
          id: 101,
          title: "Douluo Dalu",
          cover: DouLuoCover,
          synopsis: "Tang San's journey in a world of spirits.",
          status: "Ongoing",
          likes: 520,
          commentsCount: 88,
        },
        {
          id: 102,
          title: "Battle Through the Heavens",
          cover: DouPoCover,
          synopsis: "Xiao Yan rises again from the ashes.",
          status: "Ongoing",
          likes: 888,
          commentsCount: 120,
        },
        {
          id: 103,
          title: "Perfect World",
          cover: WanMeiCover,
          synopsis: "Shi Hao seeks the path to perfection.",
          status: "Finished",
          likes: 666,
          commentsCount: 95,
        },
      ],

      showCreateModal: false,
    };
  },

  methods: {
    /* Prompt for author name */
    openAuthorDialog() {
      const name = prompt("Enter your author name (≤ 7 chars):", "");
      if (!name) return;
      if (name.length > 7) {
        alert("Author name must be 7 characters or fewer.");
        return;
      }
      /* send to backend */
      axios
        .post("/api/author/name", { authorName: name })
        .catch(() => console.warn("API not ready, set locally."));
      this.authorName = name;
      this.authorNameConfirmed = true;
    },

    /* Edit chapters */
    editChapters(workId) {
      this.$router.push({ name: "ChapterEditor", params: { workId } });
    },

    /* Refresh works after creation */
    async refreshWorks() {
      try {
        const { data } = await axios.get("/api/author/works");
        this.works = data;
      } catch {
        console.warn("Refresh failed – keeping local list.");
      }
    },
  },
};
</script>

<style scoped>
/* === Layout === */
.author-dashboard-container {
  background: #fffaf0;
  min-height: 100vh;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  font-family: "Segoe UI", sans-serif;
}
.dashboard-title {
  text-align: center;
  font-size: 2rem;
  color: #a8412a;
}

/* === Author name section === */
.author-name-wrapper {
  text-align: center;
  margin: 1.4rem 0 1.8rem;
}
.set-author-btn {
  background: #f05d37;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.6rem 1.4rem;
  font-size: 1rem;
  cursor: pointer;
}
.set-author-btn:hover {
  background: #d35445;
}
.author-name-display {
  margin: 0;
  font-size: 1.4rem;
  color: #333;
}
.author-name-display span {
  color: #a8412a;
}
.author-name-note {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.3rem;
}

/* === Works area === */
.my-works-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  border-radius: 8px;
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
  font-size: 0.9rem;
  cursor: pointer;
}
.create-work-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.create-work-btn:hover:not(:disabled) {
  background: #d35445;
}
.no-works-hint {
  text-align: center;
  color: #777;
  margin-bottom: 1rem;
}
.works-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.work-card {
  display: flex;
  align-items: center;
  background: #fffcfa;
  border-radius: 6px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  gap: 1rem;
}
.work-cover {
  width: 100px;
  height: 130px;
  object-fit: cover;
  border-radius: 4px;
}
/* Stats */
.work-left-stats {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
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
/* Center */
.work-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.4rem;
}
.work-title {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}
.work-synopsis {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}
/* Edit button */
.edit-chapter-btn {
  margin-left: auto;
  background: #f05d37;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
  cursor: pointer;
}
.edit-chapter-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.edit-chapter-btn:hover:not(:disabled) {
  background: #d35445;
}
</style>
