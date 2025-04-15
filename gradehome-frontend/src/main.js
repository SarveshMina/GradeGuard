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

// Add request/response interceptors for debugging
axios.interceptors.request.use(config => {
    console.log(`Request to ${config.url}`, config);
    return config;
}, error => {
    console.error('Request error:', error);
    return Promise.reject(error);
});

axios.interceptors.response.use(response => {
    console.log(`Response from ${response.config.url}`, response);
    return response;
}, error => {
    console.error('Response error:', error);
    return Promise.reject(error);
});

const app = createApp(App)

initDarkMode()
app.use(router)
app.use(vuetify)

// Register VCalendar with a component prefix
app.use(VCalendar, {
    componentPrefix: 'vc', // Use <vc-calendar />, <vc-date-picker />, etc.
})

app.mount('#app')