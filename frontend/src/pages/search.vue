<template>
  <div class="teachers">
    <div class="search-header">
      <h2>搜索结果</h2>
      <div class="search-info" v-if="!loading && !error">
        找到 {{ teachers.length }} 个匹配结果
      </div>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="teachers.length === 0" class="no-results">
      没有找到匹配的教师
    </div>
    <div v-else class="teachers-grid">
      <div 
        v-for="teacher in teachers" 
        :key="teacher.id" 
        class="teacher-card"
        @click="navigateToTeacher(teacher.id)"
      >
        <div class="teacher-header">
          <h3>{{ teacher.name }}</h3>
          <span class="department">{{ teacher.department }}</span>
        </div>
        <div class="teacher-content">
          <div class="review-count">
            <span class="icon">📝</span>
            {{ teacher.review_count || 0 }} 条评价
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'Search',
  setup() {
    const router = useRouter()
    const route = useRoute()
    return { router, route }
  },
  data() {
    return {
      teachers: [],
      loading: true,
      error: null
    }
  },
  methods: {
    async searchTeachers() {
      try {
        this.loading = true
        const query = this.route.query.q || ''
        if (!query) {
          this.teachers = []
          this.loading = false
          return
        }
        
        const response = await axios.get(`/api/search?q=${encodeURIComponent(query)}`)
        this.teachers = response.data
        this.error = null
      } catch (err) {
        this.error = '搜索失败：' + (err.message || '未知错误')
        console.error('搜索失败:', err)
      } finally {
        this.loading = false
      }
    },
    navigateToTeacher(teacherId) {
      this.router.push(`/detail?id=${teacherId}`)
    }
  },
  watch: {
    '$route.query.q': {
      immediate: true,
      handler() {
        this.searchTeachers()
      }
    }
  }
}
</script>

<style scoped>
.teachers {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  margin-bottom: 20px;
}

.search-header h2 {
  margin: 0;
  color: #333;
}

.search-info {
  margin-top: 8px;
  color: #666;
  font-size: 0.9rem;
}

.teachers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.teacher-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.teacher-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.teacher-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.teacher-header h3 {
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

.teacher-content {
  display: flex;
  align-items: center;
}

.review-count {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 0.9rem;
}

.icon {
  font-size: 1.1rem;
}

.loading, .error, .no-results {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #f44336;
}

.no-results {
  font-size: 1.1rem;
  color: #666;
  padding: 40px 20px;
}
</style> 