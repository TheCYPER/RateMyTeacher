<template>
  <div class="profile-page">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="pa-4">
            <v-card-title class="text-h5 mb-4">个人中心</v-card-title>
            <v-card-text>
              <div class="mb-4">
                <span>用户名：</span>
                <strong>{{ userInfo.username }}</strong>
                <v-btn color="error" class="ml-4" @click="logout">退出登录</v-btn>
              </div>
              <div>
                <h3 class="text-h6 mb-2">我的所有评价</h3>
                <v-alert v-if="reviews.length === 0" type="info" border="left" class="mb-2">暂无评价</v-alert>
                <v-list v-else>
                  <v-list-item v-for="review in reviews" :key="review.id" class="mb-2">
                    <v-list-item-content>
                      <v-list-item-title>
                        <span class="font-weight-bold">{{ review.teacher_name }} - {{ review.department }}</span>
                        <v-chip color="amber" class="ml-2" small>{{ review.score }} 分</v-chip>
                      </v-list-item-title>
                      <v-list-item-subtitle class="mt-1">{{ review.comment }}</v-list-item-subtitle>
                      <div class="grey--text text--darken-1 mt-1" style="font-size: 12px;">
                        {{ formatDate(review.created_at) }}
                        <span class="ml-2">👍{{ review.likes }} 👎{{ review.dislikes }}</span>
                      </div>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuth } from '@/composables/useAuth'

export default {
  name: 'Profile',
  setup() {
    const { isLoggedIn, username, logout: doLogout } = useAuth()
    const router = useRouter()
    const userInfo = ref({ username: '' })
    const userId = ref(null)
    const reviews = ref([])

    const fetchUserInfoAndReviews = async () => {
      if (!isLoggedIn.value) {
        router.push('/login')
        return
      }
      try {
        const userRes = await axios.get(`/api/user/by-username/${username.value}`)
        userInfo.value = userRes.data
        userId.value = userRes.data.id
        const reviewsRes = await axios.get(`/api/user/reviews/${userId.value}`)
        reviews.value = reviewsRes.data
      } catch (err) {
        console.error('获取用户信息或评论失败:', err)
        router.push('/login')
      }
    }

    const logout = () => {
      doLogout()
      router.push('/login')
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const d = new Date(dateStr)
      return d.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }

    onMounted(fetchUserInfoAndReviews)

    return {
      userInfo,
      reviews,
      logout,
      formatDate
    }
  }
}
</script>

<style scoped>
.profile-page {
  padding: 20px 0;
}
</style> 