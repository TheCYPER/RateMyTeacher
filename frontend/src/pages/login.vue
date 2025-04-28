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
              :loading="loading"
              :disabled="loading"
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const username = ref('');
const password = ref('');
const loading = ref(false);

const handleLogin = async () => {
  // 表单验证
  if (!username.value || !password.value) {
    alert('请填写所有必填字段');
    return;
  }

  try {
    loading.value = true;
    const response = await axios.post('http://localhost:8000/login', {
      username: username.value,
      password: password.value
    });

    if (response.data.message === '登录成功') {
      // 更新全局登录状态
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('username', username.value);
      
      // 触发全局状态更新
      window.dispatchEvent(new CustomEvent('loginStateChanged', {
        detail: {
          isLoggedIn: true,
          username: username.value
        }
      }));

      alert('登录成功！');
      router.push('/');
    }
  } catch (error) {
    if (error.response) {
      console.error('Login error:', error.response);
      alert(`登录失败：${error.response.data.error || '请重试'}\n错误详情：${JSON.stringify(error.response.data, null, 2)}`);
    } else {
      console.error('Network error:', error);
      alert('登录失败，请检查网络连接');
    }
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style> 