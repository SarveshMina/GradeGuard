// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'          // Global styles
import vuetify from './plugins/vuetify'  // <-- import the vuetify plugin we created

createApp(App)
    .use(router)
    .use(vuetify)
    .mount('#app')
