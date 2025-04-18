<template>
    <div class="library">
      <!-- 分类筛选 -->
      <div class="filter-row">
        <span class="filter-label">分类：</span>
        <button
          v-for="cat in categories"
          :key="cat"
          :class="{ active: selectedCategory === cat }"
          @click="selectedCategory = cat"
        >
          {{ cat }}
        </button>
      </div>
  
      <!-- 排序标签 -->
      <div class="sort-tabs">
        <button
          v-for="tab in sortTabs"
          :key="tab"
          :class="{ active: selectedSort === tab }"
          @click="selectedSort = tab"
        >
          {{ tab }}
        </button>
      </div>
  
      <!-- 书籍列表 -->
      <div class="grid">
        <div
          v-for="book in sortedBooks"
          :key="book.id"
          class="book-card"
        >
          <img :src="book.cover" alt="cover" class="cover" />
          <div class="info">
            <router-link :to="`/novel/${book.id}`" class="title">
            {{ book.title }}
            </router-link>
            <div class="author">作者：{{ book.author }}</div>
            <div class="meta">{{ book.status }} · {{ book.wordCount }}万字</div>
            <div class="desc">{{ book.description }}</div>
            <div class="update">{{ book.updateTime }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  
  const categories = ["悬疑",'武侠', '奇幻', '都市', '恋爱'];
  const selectedCategory = ref(categories[0]);
  
  // 排序选项
  const sortTabs = ['最热', '最新'];
  const selectedSort = ref(sortTabs[0]);
  
  const books = ref([]);
  
  // 模拟从接口加载数据
  onMounted(() => {
     books.value = [
  {
    id: 1,
    title: '惜花芷',
    author: '林佳一',
    status: '连载中',
    wordCount: 120.5,
    cover: '/src/assets/covers/book1.jpeg',
    description: '一朝入宫，风云变幻，她如何步步为营……',
    updateTime: '2025-04-10',
    category: '恋爱'
  },
  {
    id: 2,
    title: '我不是戏神',
    author: '三九音域',
    status: '连载中',
    wordCount: 259.6,
    cover: '/src/assets/covers/book2.jpeg',
    description: '主人公穿越到虚拟世界成为一个“戏神”，不断提升自己，挑战更强大的对手。',
    updateTime: '2025-04-15',
    category: '都市'
  },
  {
    id: 3,
    title: '斩神',
    author: '月夜星辰',
    status: '已完结',
    wordCount: 320.1,
    cover: '/src/assets/covers/book3.jpeg',
    description: '一部融合了玄幻与武侠元素的小说，讲述了一个少年从零开始，逐渐成为可以斩尽天下神魔的强者。',
    updateTime: '2024-12-01',
    category: '都市'
  },
  {
    id: 4,
    title: '异兽迷城',
    author: '冰冷的笑容',
    status: '连载中',
    wordCount: 350.8,
    cover: '/src/assets/covers/book4.jpeg',
    description: '一场突如其来的灾难将城市与异兽之间的界限模糊，主人公必须面对未知的恐怖，揭开一段段埋藏的真相。',
    updateTime: '2025-03-22 ',
    category: '奇幻'
  },
  {
    id: 5,
    title: '诡舍',
    author: '杀虫队队员',
    status: '已完结',
    wordCount: 298.5,
    cover: '/src/assets/covers/book5.jpeg',
    description: '悬疑惊悚小说，讲述了几个调查员进入神秘古宅，探索未解之谜，揭开一个个可怕的秘密。',
    updateTime: '2024-11-12 ',
    category: '悬疑'
  },
  {
    id: 6,
    title: '京圈九爷',
    author: '三九音域',
    status: '已完结',
    wordCount: 150.3,
    cover: '/src/assets/covers/book6.png',
    description: '强势男性在豪门权力斗争中的成长与爱情，夹杂着权谋与心计。',
    updateTime: '2024-10-20',
    category: '恋爱'
  },
  {
    id: 7,
    title: '诸神愚戏',
    author: '一月九十秋',
    status: '连载中',
    wordCount: 210.9,
    cover: '/src/assets/covers/book7.png',
    description: '主角被卷入一场阴谋之中，逐步揭开诸神之间的真正关系。',
    updateTime: '2025-04-05',
    category: '奇幻'
  },
  {
    id: 8,
    title: '我，修仙大佬',
    author: '明月夜',
    status: '连载中',
    wordCount: 480.0,
    cover: '/src/assets/covers/book8.png',
    description: '仙侠小说，讲述了一个现代人穿越到修仙世界，从一无所有到成为世界顶尖修士的故事。',
    updateTime: '2025-03-30',
    category: '宫斗'
  },
  {
    id: 9,
    title: '好一个乖乖女',
    author: '江小晨',
    status: '已完结',
    wordCount: 215.2,
    cover: '/src/assets/covers/book9.jpeg',
    description: '这是一部现代都市爱情小说，讲述了一个乖乖女如何挑战命运，最终找到了自己的真爱。',
    updateTime: '2024-09-19',
    category: '恋爱'
  },
  {
    id: 10,
    title: '全民求生',
    author: '南风未起',
    status: '已完结',
    wordCount: 390.4,
    cover: '/src/assets/covers/book10.png',
    description: '一场突如其来的全球灾难，世界陷入危机，主角需要带领幸存者们进行艰难的求生。',
    updateTime: '2025-03-18',
    category: '都市'
  },
  {
    id: 11,
    title: '天渊',
    author: '沐潇三生',
    status: '连载中',
    wordCount: 280.6,
    cover: '/src/assets/covers/book11.jpeg',
    description: '一个关于命运和抉择的故事，主角将要挑战天命，走上一条未知的道路。',
    updateTime: '2025-04-02',
    category: '奇幻'
  },
  {
    id: 12,
    title: '摄政王',
    author: '洛羽倾',
    status: '已完结',
    wordCount: 320.0,
    cover: '/src/assets/covers/book12.png',
    description: '摄政王如何在政坛与江湖之间游走，保持着自己的力量与权威。',
    updateTime: '2024-08-13',
    category: '武侠'
  },
  {
    id: 13,
    title: '癫都癫',
    author: '莫颜',
    status: '已完结',
    wordCount: 150.5,
    cover: '/src/assets/covers/book13.png',
    description: '一个女孩如何在都市里奋斗，最终找到属于自己的幸福。',
    updateTime: '2024-05-10',
    category: '恋爱'
  },
  {
    id: 14,
    title: '洪荒',
    author: '秦云',
    status: '连载中',
    wordCount: 400.9,
    cover: '/src/assets/covers/book14.png',
    description: '一个年轻的修士在洪荒世界中的冒险与成长，以及他与世界的关系。',
    updateTime: '2025-03-25',
    category: '奇幻'
  },
  {
    id: 15,
    title: '北派盗墓',
    author: '黑猫',
    status: '已完结',
    wordCount: 550.3,
    cover: '/src/assets/covers/book15.jpeg',
    description: '一群盗墓贼如何在深山中破解古墓谜题，找寻埋藏的宝藏。',
    updateTime: '2025-02-17',
    category: '悬疑'
  },
  {
    id: 16,
    title: '北上娇娇',
    author: '尘月',
    status: '已完结',
    wordCount: 210.8,
    cover: '/src/assets/covers/book16.jpeg',
    description: '一位少女如何从一名普通职员成长为一位商业巨头，掌控自己命运的故事。',
    updateTime: '2024-06-25',
    category: '都市'
  },
  {
    id: 17,
    title: '凡骨',
    author: '楚天歌',
    status: '已完结',
    wordCount: 400.1,
    cover: '/src/assets/covers/book17.png',
    description: '仙侠小说，主人公突破种种难关，最终成就无上仙道，拯救苍生。',
    updateTime: '2024-12-01',
    category: '奇幻'
  },
  {
    id: 18,
    title: '夏夜有染',
    author: '墨灵霜',
    status: '连载中',
    wordCount: 380.2,
    cover: '/src/assets/covers/book18.jpeg',
    description: '都市浪漫小说，讲述了一段青涩的校园恋情，如何在成长中经历波折，最终走到一起。',
    updateTime: '2025-04-01',
    category: '都市'
  }
];

  });
  
  // 先按分类过滤
  const filteredBooks = computed(() =>
    books.value.filter(b => b.category === selectedCategory.value)
  );
  
  // 再按选中排序
  const sortedBooks = computed(() => {
    const list = [...filteredBooks.value];
    if (selectedSort.value === '最新') {
      return list.sort((a, b) => new Date(b.updateTime) - new Date(a.updateTime));
    } else if (selectedSort.value === '字数') {
      return list.sort((a, b) => b.wordCount - a.wordCount);
    }
    // 最热：保持原序
    return list;
  });
  </script>
  
  <style scoped>
  .library {
    margin-top: 80px;
    margin-left: 100px;
    max-width: 1200px;
    padding: 20px;
  }
  
  /* 分类筛选行 */
  .filter-row {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
  }
  .filter-label {
    font-weight: bold;
    margin-right: 12px;
  }
  .filter-row button {
    margin-right: 8px;
    padding: 6px 14px;
    border: 1px solid #ccc;
    background: white;
    border-radius: 16px;
    cursor: pointer;
    font-size: 14px;
  }
  .filter-row button.active {
    background: #ff6600;
    color: white;
    border-color: #ff6600;
  }
  
  /* 排序标签 */
  .sort-tabs {
    margin-top:20px;
    display: flex;
    border-bottom: 1px solid #eaeaea;
    margin-bottom: 20px;
  }
  .sort-tabs button {
    background: none;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    color: #333;
    position: relative;
  }
  .sort-tabs button.active {
    color: #ff6600;
  }
  .sort-tabs button.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: #ff6600;
  }
  
  /* 书籍网格 */
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
  
  /* 单个书籍卡片 */
  .book-card {
    display: flex;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    overflow: hidden;
    align-items:center;
  }
  .cover {
    width: 120px;
    height: 160px;
    object-fit: cover;
  }
  .info {
    padding: 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
  }
  .title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #333;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s;
}
.title:hover {
  color: #ff6600;
}
  .author, .meta, .update {
    font-size: 12px;
    color: #888;
    margin-bottom: 4px;
  }
  .desc {
    font-size: 12px;
    color: #555;
    flex: 1;
   display: -webkit-box;           /* 多行截断 */
   -webkit-box-orient: vertical;
   -webkit-line-clamp:1;          /* 限制两行 */
   overflow: hidden;
  }
  </style>
  
  