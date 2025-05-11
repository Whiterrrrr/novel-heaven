<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <h2 class="modal-title">Create New Work</h2>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

      <form class="create-work-form" @submit.prevent="handleSubmit">
        <!-- Title -->
        <label>Title (≤10 chars)</label>
        <input
          v-model="title"
          maxlength="10"
          placeholder="Enter title"
          required
        />

        <!-- Category -->
        <label>Category</label>
        <select v-model="selectedCategory" required>
          <option value="" disabled>Select category</option>
          <option
            v-for="cat in categories"
            :key="cat.id"
            :value="cat.id"
          >{{ cat.name }}</option>
        </select>

        <!-- Cover (JPG/PNG ≤ 2 MB) -->
        <label>Cover (JPG/PNG ≤ 2 MB)</label>
        <div class="file-wrapper">
          <input
            ref="coverInput"
            type="file"
            accept="image/png, image/jpeg"
            hidden
            @change="handleFileChange"
            required
          />
          <button
            type="button"
            class="file-btn"
            @click="triggerFileSelect"
          >Choose File</button>
          <span class="file-name">{{ fileName }}</span>
        </div>

        <!-- Preview -->
        <div v-if="previewUrl" class="preview-area">
          <img :src="previewUrl" alt="cover preview" />
          <p class="preview-caption">{{ title || "Title preview" }}</p>
        </div>

        <!-- Synopsis (≤300 chars) -->
        <label>
          Synopsis (≤300 chars)
          <span class="count">{{ synopsis.length }}/300</span>
        </label>
        <textarea
          v-model="synopsis"
          maxlength="300"
          placeholder="Enter synopsis"
          required
        ></textarea>

        <!-- Buttons -->
        <div class="button-group">
          <button type="submit" class="publish-btn">Publish</button>
          <button type="button" class="cancel-btn" @click="close">
            Cancel
          </button>
        </div>
      </form>

      <!-- Disclaimer -->
      <p class="disclaimer">
        Once created and published, the work title and cover cannot be changed.
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateWork",
  props: { visible: Boolean },
  data() {
    return {
      title: "",
      synopsis: "",
      coverFile: null,
      previewUrl: "",
      fileName: "No file chosen",
      errorMessage: "",
      categories: [
        { id: 1,  name: "Fantasy"         },
        { id: 2,  name: "Urban"           },
        { id: 3,  name: "SciFi"           },
        { id: 4,  name: "Wuxia"           },
        { id: 5,  name: "Thriller"        },
        { id: 6,  name: "Historical"      },
        { id: 7,  name: "Gaming"          },
        { id: 8,  name: "ACGN"            },
        { id: 9,  name: "WesternFantasy"  },
        { id: 10, name: "Infinite"        },
        { id: 11, name: "SystemTravel"    },
        { id: 12, name: "AncientRomance"  },
        { id: 13, name: "Mecha"           },
        { id: 14, name: "Cthulhu"         },
        { id: 15, name: "Others"          },
      ],
      selectedCategory: "",
    };
  },
  methods: {
    triggerFileSelect() {
      this.$refs.coverInput.click();
    },
    handleFileChange(e) {
      const file = e.target.files[0];
      if (!file) return;
      if (!["image/png", "image/jpeg"].includes(file.type)) {
        return this.showErr("Only JPG or PNG images are allowed.");
      }
      if (file.size > 2 * 1024 * 1024) {
        return this.showErr("Image size must be ≤ 2 MB.");
      }
      this.errorMessage = "";
      this.coverFile = file;
      this.previewUrl = URL.createObjectURL(file);
      this.fileName = file.name;
    },
    async handleSubmit() {
      if (!this.title.trim() || !this.synopsis.trim()) {
        return this.showErr("Title and synopsis cannot be empty.");
      }
      if (this.title.length > 10) {
        return this.showErr("Title must be 10 characters or fewer.");
      }
      if (!this.coverFile) {
        return this.showErr("Cover image is required.");
      }
      if (!this.selectedCategory) {
        return this.showErr("Please select a category.");
      }

      const fd = new FormData();
      fd.append("title", this.title);
      fd.append("synopsis", this.synopsis);
      fd.append("cover", this.coverFile);
      fd.append("category_id", this.selectedCategory);

      try {
        const { data } = await axios.post(
          "/api/author/works",
          fd,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${localStorage.token}`,
            },
          }
        );
        this.resetAndClose();
        this.$emit("created", data);
      } catch {
        this.showErr("Failed to create work. Please try again.");
      }
    },
    showErr(msg) {
      this.errorMessage = msg;
    },
    close() {
      this.resetAndClose();
    },
    resetAndClose() {
      this.title = "";
      this.synopsis = "";
      this.coverFile = null;
      this.previewUrl = "";
      this.fileName = "No file chosen";
      this.errorMessage = "";
      this.selectedCategory = "";
      this.$emit("update:visible", false);
    },
  },
};
</script>

<style scoped>
/* 弹窗更宽：960px */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.modal-content {
  background: #fff;
  width: 960px;
  max-width: 700px;
  padding: 2.4rem;
  border-radius: 10px;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25);
}
.modal-title {
  text-align: center;
  margin-bottom: 1.2rem;
  font-size: 1.5rem;
  color: #a8412a;
}
.error-text {
  color: #e74c3c;
  text-align: center;
  margin-bottom: 0.6rem;
}

.create-work-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Input & Textarea 基础样式 */
.create-work-form input,
.create-work-form textarea {
  padding: 0.7rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.create-work-form input:focus,
.create-work-form textarea:focus {
  outline: none;
  border-color: #a8412a;
  box-shadow: 0 0 4px rgba(168, 65, 42, 0.4);
}

/* Category 下拉框 全宽 */
.create-work-form select {
  width: 100%;
  padding: 0.7rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  transition: box-shadow 0.2s, border-color 0.2s;
  box-sizing: border-box;
}

/* Synopsis 文本框 特别宽 & 高度放大 */
.create-work-form textarea {
  width: 100%;
  min-height: 300px;
  resize: vertical;
  box-sizing: border-box;
}

/* File upload */
.file-wrapper {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.file-btn {
  background: #666;
  color: #fff;
  border: none;
  padding: 0.55rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.file-btn:hover {
  background: #555;
}
.file-name {
  font-size: 0.9rem;
  color: #444;
  max-width: 360px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Preview */
.preview-area {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.preview-area img {
  width: 110px;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}
.preview-caption {
  font-size: 1rem;
  color: #333;
}

/* Buttons 居中 */
.button-group {
  display: flex;
  justify-content: center;
  gap: 1.4rem;
  margin-top: 0.6rem;
}
.publish-btn,
.cancel-btn {
  border: none;
  padding: 0.9rem 1.7rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.publish-btn {
  background: #f05d37;
  color: #fff;
}
.publish-btn:hover {
  background: #d35445;
}
.cancel-btn {
  background: #bbb;
  color: #fff;
}
.cancel-btn:hover {
  background: #999;
}

/* Misc */
.count {
  font-size: 0.8rem;
  color: #777;
  margin-left: 0.4rem;
}
.disclaimer {
  margin-top: 1.2rem;
  font-size: 0.85rem;
  color: #a8412a;
  text-align: center;
}
</style>
