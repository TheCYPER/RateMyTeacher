<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="username"
                label="Username"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="email"
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="email"
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

              <v-text-field
                v-model="confirmPassword"
                label="Confirm Password"
                name="confirmPassword"
                prepend-icon="mdi-lock-check"
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
              @click="handleRegister"
            >
              Register
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            Already have an account? 
            <a
              href="#"
              class="text-decoration-none"
              style="color: #4CAF50;"
              @click.prevent="goToLogin"
            >
              Login here
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
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);

const handleRegister = async () => {
  // 表单验证
  if (!username.value || !password.value || !confirmPassword.value) {
    alert('请填写所有必填字段');
    return;
  }

  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致');
    return;
  }

  try {
    loading.value = true;
    const response = await axios.post('/register', {
      username: username.value,
      password: password.value,
      school: '未知学校' // 默认值
    });

    if (response.data.message === '注册成功') {
      alert('注册成功！请登录');
      router.push('/login');
    }
  } catch (error) {
    if (error.response) {
      // 服务器返回的错误信息
      console.error('Registration error:', error.response);
      alert(`注册失败：${error.response.data.error || '请重试'}\n错误详情：${JSON.stringify(error.response.data, null, 2)}`);
    } else {
      // 网络错误等
      console.error('Network error:', error);
      alert('注册失败，请检查网络连接');
    }
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style> 