<template>
    <div class="comment-section">
      <h2>Comments</h2>
      <ul>
        <li v-for="(comment, index) in comments" :key="index">
          {{ comment }}
        </li>
      </ul>
      <input v-model="newComment" placeholder="Write a comment..." />
      <button @click="addComment">Add Comment</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        comments: ["Great novel!", "I love this story!"],
        newComment: "",
      };
    },
    methods: {
      addComment() {
        if (this.newComment.trim()) {
          this.comments.push(this.newComment);
          this.newComment = "";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .comment-section {
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 5px;
  }
  input {
    margin-top: 10px;
    padding: 5px;
  }
  </style>