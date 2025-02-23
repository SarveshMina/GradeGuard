// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'          // Global styles
import vuetify from './plugins/vuetify'
import axios from 'axios'

// Set Axios defaults to send cookies with every request.
axios.defaults.withCredentials = true

createApp(App)
    .use(router)
    .use(vuetify)
    .mount('#app')
