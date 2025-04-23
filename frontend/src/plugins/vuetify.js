/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#009688', // teal
          secondary: '#26A69A', // teal-lighten-1
          accent: '#4DB6AC', // teal-lighten-2
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        },
      },
      dark: {
        colors: {
          primary: '#4DB6AC', // teal-lighten-2 - 更亮的颜色，适合深色背景
          secondary: '#80CBC4', // teal-lighten-3 - 更亮的次要颜色
          accent: '#B2DFDB', // teal-lighten-4 - 最亮的强调色
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        },
      },
    },
  },
})
