<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <!-- 移动端菜单按钮 -->
      <v-app-bar-nav-icon v-if="isMobile" @click="drawer = !drawer"></v-app-bar-nav-icon>
      
      <!-- 左侧区域：标题和导航按钮 -->
      <div class="d-flex align-center ml-4">
        <v-toolbar-title class="hidden-xs-only">Rate My Teacher</v-toolbar-title>
        
        <!-- 桌面端导航链接 - 紧贴标题右侧 -->
        <div class="hidden-sm-and-down ml-4">
          <v-btn text to="/" class="mr-2">Home</v-btn>
          <v-btn text to="/teachers" class="mr-2">List of Teachers</v-btn>
        </div>
      </div>
      
      <v-spacer></v-spacer>
      
      <!-- 搜索栏 -->
      <v-text-field
        v-if="isLoggedIn"
        v-model="searchQuery"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        class="mx-4"
        style="max-width: 300px;"
        @keyup.enter="handleSearch"
      ></v-text-field>
      
      <!-- 用户信息/登录按钮 -->
      <div v-if="isLoggedIn" class="mr-4">
        <v-btn text @click="goToProfile">
          <v-icon left>mdi-account</v-icon>
          {{ username }}
        </v-btn>
      </div>
      <div v-else class="mr-4">
        <v-btn text @click="goToLogin">
          Log in / Sign up
        </v-btn>
      </div>
    </v-app-bar>
    
    <!-- 移动端导航抽屉 -->
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <v-list-item to="/">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        
        <v-list-item to="/teachers">
          <v-list-item-icon>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>List of Teachers</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    
  <v-main>
    <router-view />
  </v-main>

  <AppFooter />
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import AppFooter from '@/components/AppFooter.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 全局状态变量 - 用户登录状态
const isLoggedIn = ref(false);
const username = ref('');
const searchQuery = ref('');
const drawer = ref(false);

// 初始化登录状态
onMounted(() => {
  // 从 localStorage 读取登录状态
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
  username.value = localStorage.getItem('username') || '';

  // 监听登录状态变化
  window.addEventListener('loginStateChanged', handleLoginStateChange);
});

// 清理事件监听
onUnmounted(() => {
  window.removeEventListener('loginStateChanged', handleLoginStateChange);
});

// 处理登录状态变化
const handleLoginStateChange = (event) => {
  isLoggedIn.value = event.detail.isLoggedIn;
  username.value = event.detail.username;
};

// 响应式设计 - 检测是否为移动设备
const isMobile = computed(() => {
  return window.innerWidth < 600;
});

// 导航函数
const goToLogin = () => {
  router.push('/register');
};

const goToProfile = () => {
  router.push('/profile');
};

const handleSearch = () => {
  console.log('Search for:', searchQuery.value);
};
</script>

<style scoped>
.hidden-xs-only {
  display: none;
}

@media (min-width: 600px) {
  .hidden-xs-only {
    display: block;
  }
}

.hidden-sm-and-down {
  display: none;
}

@media (min-width: 960px) {
  .hidden-sm-and-down {
    display: block;
  }
}
</style>
