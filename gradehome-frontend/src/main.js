import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'  // Global styles

createApp(App)
    .use(router)
    .mount('#app')
