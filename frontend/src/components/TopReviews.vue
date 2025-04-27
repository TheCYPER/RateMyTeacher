<template>
  <div class="top-reviews">
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
        const response = await axios.get('http://localhost:8000/api/reviews/top')
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
  font-size: 1.2rem;
  color: #333;
}

.department {
  font-size: 0.9rem;
  color: #666;
  background-color: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
}

.review-content {
  margin-bottom: 15px;
}

.score {
  font-weight: bold;
  color: #009688;
  margin-bottom: 8px;
}

.comment {
  margin: 0;
  line-height: 1.5;
  color: #444;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

.interactions {
  display: flex;
  gap: 15px;
}

.likes, .dislikes {
  cursor: pointer;
}

.date {
  font-size: 0.8rem;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #f44336;
}
</style> 