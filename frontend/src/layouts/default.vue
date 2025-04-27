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
import { ref, computed } from 'vue';
import AppFooter from '@/components/AppFooter.vue';

// 全局状态变量 - 用户登录状态
const isLoggedIn = ref(false); // 设置为false显示登录按钮，true显示用户名
const username = ref('John Doe'); // 占位符用户名
const searchQuery = ref('');
const drawer = ref(false);

// 响应式设计 - 检测是否为移动设备
const isMobile = computed(() => {
  return window.innerWidth < 600;
});

// 导航函数
const goToLogin = () => {
  // 跳转到登录页面的函数
  console.log('Navigate to login page');
  // 实际项目中可以使用 router.push('/login')
};

const goToProfile = () => {
  // 跳转到用户资料页面的函数
  console.log('Navigate to profile page');
  // 实际项目中可以使用 router.push('/profile')
};

const handleSearch = () => {
  // 处理搜索的函数
  console.log('Search for:', searchQuery.value);
  // 实际项目中可以实现搜索逻辑
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
