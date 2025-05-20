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

import { API_BASE_URL } from './config'

// 配置 axios
axios.defaults.baseURL = API_BASE_URL
axios.defaults.withCredentials = true

const app = createApp(App)

registerPlugins(app)
app.use(router)

app.mount('#app')
