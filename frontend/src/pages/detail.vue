<template>
  <div class="teacher-detail">
    <!-- 教师基本信息卡片 -->
    <div class="teacher-info-card">
      <div class="teacher-header">
        <h1>{{ teacher.name }}</h1>
        <span class="department">{{ teacher.department }}</span>
      </div>
      <div class="teacher-stats">
        <div class="stat-item">
          <span class="icon">📝</span>
          <span class="count">{{ teacher.review_count || 0 }}</span>
          <span class="label">条评价</span>
        </div>
      </div>
      <v-btn
        color="primary"
        class="write-review-btn"
        :to="`/comments?id=${teacher.id}`"
      >
        写评价
      </v-btn>
    </div>

    <!-- 评价列表 -->
    <div class="reviews-section">
      <h2>评价列表</h2>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="reviews.length === 0" class="no-reviews">
        暂无评价
      </div>
      <div v-else class="reviews-list">
        <div v-for="review in reviews" :key="review.id" class="review-card">
          <div class="review-header">
            <div class="reviewer-info">
              <span class="reviewer-name">{{ review.reviewer_name }}</span>
              <span class="review-date">{{ formatDate(review.created_at) }}</span>
            </div>
            <div class="review-rating">
              <span class="rating-label">评分：</span>
              <span class="rating-value">{{ review.rating }}</span>
            </div>
          </div>
          <div class="review-content">
            {{ review.content }}
          </div>
          <div class="review-actions">
            <div class="action-buttons">
              <v-btn
                text
                small
                :color="review.user_liked ? 'primary' : ''"
                @click="handleLike(review)"
              >
                <v-icon left class="mr-1">mdi-thumb-up</v-icon>
                {{ review.likes }}
              </v-btn>
              <v-btn
                text
                small
                :color="review.user_disliked ? 'error' : ''"
                @click="handleDislike(review)"
              >
                <v-icon left class="mr-1">mdi-thumb-down</v-icon>
                {{ review.dislikes }}
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

export default {
  name: 'TeacherDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const teacher = ref({})
    const reviews = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchTeacherDetails = async () => {
      try {
        const response = await axios.get(`/api/teachers/${route.query.id}`)
        teacher.value = response.data
      } catch (err) {
        error.value = '获取教师信息失败：' + (err.message || '未知错误')
        console.error('获取教师信息失败:', err)
      }
    }

    const fetchReviews = async () => {
      try {
        const response = await axios.get(`/api/teachers/${route.query.id}/reviews`)
        reviews.value = response.data
      } catch (err) {
        error.value = '获取评价失败：' + (err.message || '未知错误')
        console.error('获取评价失败:', err)
      } finally {
        loading.value = false
      }
    }

    const handleLike = async (review) => {
      try {
        await axios.post(`/api/reviews/${review.id}/like`)
        // 更新本地状态
        if (review.user_liked) {
          review.likes--
          review.user_liked = false
        } else {
          review.likes++
          review.user_liked = true
          if (review.user_disliked) {
            review.dislikes--
            review.user_disliked = false
          }
        }
      } catch (err) {
        console.error('点赞失败:', err)
      }
    }

    const handleDislike = async (review) => {
      try {
        await axios.post(`/api/reviews/${review.id}/dislike`)
        // 更新本地状态
        if (review.user_disliked) {
          review.dislikes--
          review.user_disliked = false
        } else {
          review.dislikes++
          review.user_disliked = true
          if (review.user_liked) {
            review.likes--
            review.user_liked = false
          }
        }
      } catch (err) {
        console.error('点踩失败:', err)
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      if (!route.query.id) {
        router.push('/teachers')
        return
      }
      fetchTeacherDetails()
      fetchReviews()
    })

    return {
      teacher,
      reviews,
      loading,
      error,
      handleLike,
      handleDislike,
      formatDate
    }
  }
}
</script>

<style scoped>
.teacher-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.teacher-info-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.teacher-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.teacher-header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.department {
  font-size: 1rem;
  color: #666;
  background-color: #f5f5f5;
  padding: 6px 12px;
  border-radius: 4px;
}

.teacher-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon {
  font-size: 1.2rem;
}

.count {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
}

.label {
  color: #666;
}

.write-review-btn {
  margin-top: 16px;
}

.reviews-section {
  margin-top: 32px;
}

.reviews-section h2 {
  margin-bottom: 20px;
  color: #333;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.reviewer-info {
  display: flex;
  flex-direction: column;
}

.reviewer-name {
  font-weight: 500;
  color: #333;
}

.review-date {
  font-size: 0.9rem;
  color: #666;
}

.review-rating {
  display: flex;
  align-items: center;
  gap: 4px;
}

.rating-label {
  color: #666;
}

.rating-value {
  font-weight: 500;
  color: #333;
}

.review-content {
  color: #333;
  line-height: 1.6;
  margin-bottom: 16px;
}

.review-actions {
  display: flex;
  justify-content: flex-end;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.loading, .error, .no-reviews {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #f44336;
}

.no-reviews {
  font-size: 1.1rem;
  padding: 40px 20px;
}
</style> 