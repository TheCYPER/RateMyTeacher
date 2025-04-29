/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Composables
import { createApp } from 'vue'

// 配置 axios
axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.withCredentials = true  // 允许跨域请求携带凭证

const app = createApp(App)

registerPlugins(app)
app.use(router)

app.mount('#app')
