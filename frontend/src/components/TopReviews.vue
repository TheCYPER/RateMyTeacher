<template>
  <div class="top-reviews">
    <h2>热门评价</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="reviews-list">
      <div v-for="review in reviews" :key="review.id" class="review-card">
        <div class="review-header">
          <h3>{{ review.teacher_name }}</h3>
          <span class="department">{{ review.department }}</span>
        </div>
        <div class="review-content">
          <div class="score">评分：{{ review.score }}分</div>
          <p class="comment">{{ review.comment }}</p>
        </div>
        <div class="review-footer">
          <div class="interactions">
            <span class="likes">👍 {{ review.likes }}</span>
            <span class="dislikes">👎 {{ review.dislikes }}</span>
          </div>
          <div class="date">{{ formatDate(review.created_at) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TopReviews',
  data() {
    return {
      reviews: [],
      loading: true,
      error: null
    }
  },
  methods: {
    async fetchTopReviews() {
      try {
        this.loading = true
        const response = await axios.get('http://localhost:5000/api/reviews/top')
        this.reviews = response.data
        this.error = null
      } catch (err) {
        this.error = '获取热门评价失败：' + (err.message || '未知错误')
        console.error('获取热门评价失败:', err)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  mounted() {
    this.fetchTopReviews()
  }
}
</script>

<style scoped>
.top-reviews {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.review-header h3 {
  margin: 0;
  color: #333;
}

.department {
  color: #666;
  font-size: 0.9em;
}

.review-content {
  margin-bottom: 15px;
}

.score {
  color: #f39c12;
  font-weight: bold;
  margin-bottom: 8px;
}

.comment {
  color: #444;
  line-height: 1.5;
  margin: 0;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
  font-size: 0.9em;
}

.interactions {
  display: flex;
  gap: 15px;
}

.likes, .dislikes {
  cursor: pointer;
}

.loading {
  text-align: center;
  color: #666;
  padding: 20px;
}

.error {
  color: #e74c3c;
  text-align: center;
  padding: 20px;
}
</style> 