<template>
  <div class="latest-reviews">
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
            <span 
              class="likes" 
              :class="{ 'active': userReactions[review.id] === 'like' }"
              @click="handleLike(review)"
            >👍 {{ review.likes }}</span>
            <span 
              class="dislikes" 
              :class="{ 'active': userReactions[review.id] === 'dislike' }"
              @click="handleDislike(review)"
            >👎 {{ review.dislikes }}</span>
          </div>
          <div class="date">{{ formatDate(review.created_at) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useAuth } from '@/composables/useAuth'

export default {
  name: 'LatestReviews',
  setup() {
    const { isLoggedIn, checkLoginStatus } = useAuth()
    return { isLoggedIn, checkLoginStatus }
  },
  data() {
    return {
      reviews: [],
      loading: true,
      error: null,
      userReactions: {} // 存储用户对每条评论的反应状态
    }
  },
  methods: {
    async fetchLatestReviews() {
      try {
        this.loading = true
        const response = await axios.get('/api/reviews/latest')
        this.reviews = response.data
        this.error = null
      } catch (err) {
        this.error = '获取最新评价失败：' + (err.message || '未知错误')
        console.error('获取最新评价失败:', err)
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
    },
    async handleLike(review) {
      try {
        // 检查用户是否已登录
        if (!this.isLoggedIn) {
          alert('请先登录后再点赞');
          return;
        }
        
        // 验证登录状态
        const isValid = await this.checkLoginStatus();
        if (!isValid) {
          alert('登录已过期，请重新登录');
          return;
        }
        
        if (this.userReactions[review.id] === 'like') {
          // 如果已经点赞，则取消点赞
          review.likes--
          this.userReactions[review.id] = null
        } else {
          // 如果已经点踩，则取消点踩并点赞
          if (this.userReactions[review.id] === 'dislike') {
            review.dislikes--
          }
          const response = await axios.post(`/api/reviews/${review.id}/like`)
          review.likes = response.data.likes
          this.userReactions[review.id] = 'like'
        }
      } catch (err) {
        console.error('点赞失败:', err)
        if (err.response && err.response.status === 401) {
          alert('请先登录后再点赞');
        } else {
          // 恢复原状态
          this.fetchLatestReviews()
        }
      }
    },
    async handleDislike(review) {
      try {
        // 检查用户是否已登录
        if (!this.isLoggedIn) {
          alert('请先登录后再点踩');
          return;
        }
        
        // 验证登录状态
        const isValid = await this.checkLoginStatus();
        if (!isValid) {
          alert('登录已过期，请重新登录');
          return;
        }
        
        if (this.userReactions[review.id] === 'dislike') {
          // 如果已经点踩，则取消点踩
          review.dislikes--
          this.userReactions[review.id] = null
        } else {
          // 如果已经点赞，则取消点赞并点踩
          if (this.userReactions[review.id] === 'like') {
            review.likes--
          }
          const response = await axios.post(`/api/reviews/${review.id}/dislike`)
          review.dislikes = response.data.dislikes
          this.userReactions[review.id] = 'dislike'
        }
      } catch (err) {
        console.error('点踩失败:', err)
        if (err.response && err.response.status === 401) {
          alert('请先登录后再点踩');
        } else {
          // 恢复原状态
          this.fetchLatestReviews()
        }
      }
    }
  },
  mounted() {
    this.fetchLatestReviews()
  }
}
</script>

<style scoped>
.latest-reviews {
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
  transition: all 0.3s ease;
  padding: 4px 8px;
  border-radius: 4px;
}

.likes:hover, .dislikes:hover {
  background-color: #f5f5f5;
}

.likes.active {
  color: #4CAF50;
  background-color: #E8F5E9;
}

.dislikes.active {
  color: #F44336;
  background-color: #FFEBEE;
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