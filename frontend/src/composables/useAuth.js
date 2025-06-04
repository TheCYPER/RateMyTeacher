import { ref, onMounted } from 'vue';
import axios from 'axios';

// 创建响应式状态
const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true');
const username = ref(localStorage.getItem('username') || '');
const userId = ref(localStorage.getItem('userId') || '');
const isLoading = ref(false);

// 检查登录状态
const checkLoginStatus = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('/protected', { withCredentials: true });
    if (response.data.message === '您已登录') {
      console.log('登录状态验证成功');
      // 更新本地存储的用户信息
      localStorage.setItem('userId', response.data.user.id);
      localStorage.setItem('username', response.data.user.username);
      userId.value = response.data.user.id;
      username.value = response.data.user.username;
      return true;
    }
  } catch (error) {
    console.error('登录状态验证失败:', error);
    // 如果验证失败，清除本地存储的登录状态
    logout();
    return false;
  } finally {
    isLoading.value = false;
  }
};

// 登录
const login = async (usernameValue, password) => {
  try {
    isLoading.value = true;
    const response = await axios.post('/login', {
      username: usernameValue,
      password: password
    }, { withCredentials: true });

    if (response.data.message === '登录成功') {
      // 更新全局登录状态
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('username', response.data.user.username);
      localStorage.setItem('userId', response.data.user.id);
      
      isLoggedIn.value = true;
      username.value = response.data.user.username;
      userId.value = response.data.user.id;
      
      // 验证登录状态
      const isValid = await checkLoginStatus();
      if (!isValid) {
        throw new Error('登录状态验证失败');
      }
      
      // 触发登录状态变化事件
      window.dispatchEvent(new CustomEvent('loginStateChanged', {
        detail: {
          isLoggedIn: true,
          username: response.data.user.username,
          userId: response.data.user.id
        }
      }));
      
      return true;
    }
    return false;
  } catch (error) {
    console.error('Login error:', error);
    logout(); // 登录失败时清除状态
    return false;
  } finally {
    isLoading.value = false;
  }
};

// 登出
const logout = () => {
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('username');
  localStorage.removeItem('userId');
  isLoggedIn.value = false;
  username.value = '';
  userId.value = '';
  
  // 触发登录状态变化事件
  window.dispatchEvent(new CustomEvent('loginStateChanged', {
    detail: {
      isLoggedIn: false,
      username: '',
      userId: ''
    }
  }));
};

// 初始化时检查登录状态
onMounted(async () => {
  if (isLoggedIn.value) {
    const isValid = await checkLoginStatus();
    if (!isValid) {
      logout();
    }
  }
});

export function useAuth() {
  return {
    isLoggedIn,
    username,
    userId,
    isLoading,
    login,
    logout,
    checkLoginStatus
  };
} 