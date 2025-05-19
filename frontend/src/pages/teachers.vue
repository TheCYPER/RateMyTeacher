<template>
  <div class="teachers">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
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
import { useRouter } from 'vue-router'

export default {
  name: 'Teachers',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      teachers: [],
      loading: true,
      error: null
    }
  },
  methods: {
    async fetchTeachers() {
      try {
        this.loading = true
        const response = await axios.get('/api/teachers')
        this.teachers = response.data
        this.error = null
      } catch (err) {
        this.error = '获取教师列表失败：' + (err.message || '未知错误')
        console.error('获取教师列表失败:', err)
      } finally {
        this.loading = false
      }
    },
    navigateToTeacher(teacherId) {
      this.router.push(`/detail?id=${teacherId}`)
    }
  },
  mounted() {
    this.fetchTeachers()
  }
}
</script>

<style scoped>
.teachers {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
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

.loading, .error {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #f44336;
}
</style> 