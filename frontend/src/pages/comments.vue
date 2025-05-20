<template>
  <div class="comments-page">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="pa-4">
            <v-card-title class="text-h5 mb-4">
              {{ teacherId ? '写评价' : '选择教师并写评价' }}
            </v-card-title>

            <!-- 教师选择部分 -->
            <div v-if="!teacherId" class="mb-6">
              <v-autocomplete
                v-model="selectedTeacher"
                :items="teachers"
                item-title="name"
                item-value="id"
                label="选择教师"
                :loading="loadingTeachers"
                :error-messages="teacherError"
                return-object
                @update:search="searchTeachers"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props">
                    <v-list-item-title>{{ item.raw.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.raw.department }}</v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-autocomplete>

              <!-- 新教师表单 -->
              <div v-if="showNewTeacherForm" class="mt-4">
                <v-text-field
                  v-model="newTeacher.name"
                  label="教师姓名"
                  :rules="[v => !!v || '请输入教师姓名']"
                  class="mb-2"
                ></v-text-field>
                <v-text-field
                  v-model="newTeacher.department"
                  label="所属院系"
                  :rules="[v => !!v || '请输入所属院系']"
                ></v-text-field>
              </div>
            </div>

            <!-- 评价表单 -->
            <v-form ref="form" v-model="valid" @submit.prevent="submitReview">
              <v-rating
                v-model="score"
                color="amber"
                density="compact"
                hover
                size="large"
                class="mb-4"
                :rules="[v => v > 0 || '请选择评分']"
              ></v-rating>

              <v-textarea
                v-model="comment"
                label="评价内容"
                :rules="[v => !!v || '请输入评价内容']"
                rows="4"
                class="mb-4"
              ></v-textarea>

              <v-btn
                color="primary"
                type="submit"
                :loading="submitting"
                :disabled="!valid || submitting || (!teacherId && !selectedTeacher && !showNewTeacherForm)"
                block
              >
                提交评价
              </v-btn>
            </v-form>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuth } from '@/composables/useAuth'

export default {
  name: 'Comments',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const { isLoggedIn, username } = useAuth()
    
    const form = ref(null)
    const valid = ref(false)
    const score = ref(0)
    const comment = ref('')
    const submitting = ref(false)
    const teachers = ref([])
    const selectedTeacher = ref(null)
    const loadingTeachers = ref(false)
    const teacherError = ref('')
    const showNewTeacherForm = ref(false)
    const userId = ref(null)

    const newTeacher = ref({
      name: '',
      department: ''
    })

    const teacherId = ref(route.query.id || null)

    // 获取用户ID
    const fetchUserId = async () => {
      try {
        // 先检查是否已登录
        const response = await axios.get('/protected')
        if (response.data.message === '您已登录') {
          // 如果已登录，获取用户信息
          const userResponse = await axios.get(`/api/user/by-username/${username.value}`)
          userId.value = userResponse.data.id
        } else {
          throw new Error('未登录')
        }
      } catch (err) {
        console.error('获取用户ID失败:', err)
        router.push('/login')
      }
    }

    const searchTeachers = async (search) => {
      if (!search) return
      try {
        loadingTeachers.value = true
        const response = await axios.get(`/api/teachers/search?q=${search}`)
        teachers.value = response.data
        showNewTeacherForm.value = false
      } catch (err) {
        teacherError.value = '搜索教师失败：' + (err.message || '未知错误')
        console.error('搜索教师失败:', err)
      } finally {
        loadingTeachers.value = false
      }
    }

    const fetchTeacherDetails = async (id) => {
      try {
        const response = await axios.get(`/api/teachers/${id}`)
        selectedTeacher.value = response.data
      } catch (err) {
        console.error('获取教师信息失败:', err)
        router.push('/teachers')
      }
    }

    const addNewTeacher = async () => {
      try {
        const response = await axios.post('/api/teachers', {
          name: newTeacher.value.name,
          department: newTeacher.value.department
        })
        return response.data
      } catch (err) {
        console.error('添加教师失败:', err)
        throw err
      }
    }

    const validateForm = () => {
      if (score.value === 0) {
        teacherError.value = '请选择评分'
        return false
      }
      if (!comment.value) {
        teacherError.value = '请输入评价内容'
        return false
      }
      if (!teacherId.value && !selectedTeacher.value && !showNewTeacherForm.value) {
        teacherError.value = '请选择或创建教师'
        return false
      }
      if (showNewTeacherForm.value && (!newTeacher.value.name || !newTeacher.value.department)) {
        teacherError.value = '请填写完整的教师信息'
        return false
      }
      return true
    }

    const submitReview = async () => {
      if (!validateForm()) return
      if (!isLoggedIn.value) {
        router.push('/login')
        return
      }
      if (!userId.value) {
        teacherError.value = '无法获取用户信息，请重新登录'
        return
      }

      try {
        submitting.value = true
        let teacherData = {}

        // 处理教师信息
        if (teacherId.value) {
          // 已有教师ID的情况
          if (!selectedTeacher.value) {
            throw new Error('无法获取教师信息')
          }
          teacherData = {
            teacher_id: teacherId.value,
            teacher_name: selectedTeacher.value.name,
            department: selectedTeacher.value.department
          }
        } else if (selectedTeacher.value) {
          // 从搜索结果选择教师
          teacherData = {
            teacher_id: selectedTeacher.value.id,
            teacher_name: selectedTeacher.value.name,
            department: selectedTeacher.value.department
          }
        } else if (showNewTeacherForm.value) {
          // 新教师的情况
          if (!newTeacher.value.name || !newTeacher.value.department) {
            throw new Error('请填写完整的教师信息')
          }
          const newTeacherResult = await addNewTeacher()
          teacherData = {
            teacher_name: newTeacher.value.name,
            department: newTeacher.value.department
          }
          if (newTeacherResult.id) {
            teacherData.teacher_id = newTeacherResult.id
          }
        } else {
          throw new Error('请选择或创建教师')
        }

        // 提交评价
        const reviewData = {
          score: score.value,
          comment: comment.value,
          user_id: userId.value,
          ...teacherData
        }

        const response = await axios.post('/api/reviews', reviewData)
        if (response.data.id) {
          router.push(`/detail?id=${teacherData.teacher_id || ''}`)
        } else {
          throw new Error('提交评价失败')
        }
      } catch (err) {
        console.error('提交评价失败:', err)
        teacherError.value = '提交评价失败：' + (err.message || '未知错误')
      } finally {
        submitting.value = false
      }
    }

    // 监听搜索输入，如果没有结果则显示新教师表单
    const handleSearch = async (search) => {
      await searchTeachers(search)
      if (search && teachers.value.length === 0) {
        showNewTeacherForm.value = true
        newTeacher.value.name = search
      }
    }

    onMounted(async () => {
      if (teacherId.value) {
        await fetchTeacherDetails(teacherId.value)
      }
      if (isLoggedIn.value) {
        await fetchUserId()
      }
    })

    return {
      form,
      valid,
      score,
      comment,
      submitting,
      teachers,
      selectedTeacher,
      loadingTeachers,
      teacherError,
      teacherId,
      showNewTeacherForm,
      newTeacher,
      searchTeachers: handleSearch,
      submitReview
    }
  }
}
</script>

<style scoped>
.comments-page {
  padding: 20px 0;
}
</style> 