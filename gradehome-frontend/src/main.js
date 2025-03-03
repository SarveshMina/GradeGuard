// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'  // your global styles
import vuetify from './plugins/vuetify'
import axios from 'axios'
import { initDarkMode } from './services/darkModeService'

// IMPORT the default VCalendar stylesheet:
import 'v-calendar/style.css'

// Next, import VCalendar itself:
import VCalendar from 'v-calendar'

// Set Axios defaults to send cookies with every request
axios.defaults.withCredentials = true

const app = createApp(App)

initDarkMode()
app.use(router)
app.use(vuetify)

// Register VCalendar with a component prefix
app.use(VCalendar, {
    componentPrefix: 'vc', // Use <vc-calendar />, <vc-date-picker />, etc.
})

app.mount('#app')
