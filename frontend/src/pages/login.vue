<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Username"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center pb-4">
            <v-btn
              color="primary"
              size="large"
              min-width="200"
              elevation="2"
              :loading="isLoading"
              :disabled="isLoading"
              @click="handleLogin"
            >
              Login
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            Don't have an account? 
            <a
              href="#"
              class="text-decoration-none"
              style="color: #4CAF50;"
              @click.prevent="goToRegister"
            >
              Register here
            </a>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const username = ref('');
const password = ref('');
const { login, isLoading, checkLoginStatus } = useAuth();

const handleLogin = async () => {
  // 表单验证
  if (!username.value || !password.value) {
    alert('请填写所有必填字段');
    return;
  }

  try {
    const success = await login(username.value, password.value);
    
    if (success) {
      alert('登录成功！');
      router.push('/');
    } else {
      alert('登录失败，请检查用户名和密码');
    }
  } catch (error) {
    console.error('Login error:', error);
    alert('登录失败，请重试');
  }
};

// 页面加载时检查登录状态
onMounted(async () => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
  if (isLoggedIn) {
    const isValid = await checkLoginStatus();
    if (isValid) {
      router.push('/');
    }
  }
});

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style> 