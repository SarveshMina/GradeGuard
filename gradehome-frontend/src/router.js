import { createRouter, createWebHistory } from 'vue-router'
import Landing from './views/Landing.vue'
import Login from './views/Login.vue'
import ForgotPassword from './views/ForgotPassword.vue'
import MobileLanding from './views/MobileLanding.vue'
import { Capacitor } from '@capacitor/core'

// You can detect a mobile build via Capacitor or use screen width
const isMobileApp = Capacitor.isNativePlatform() || window.innerWidth <= 768

const routes = [
    {
        path: '/',
        name: 'Home',
        component: isMobileApp ? MobileLanding : Landing, // Use MobileLanding on mobile
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
        path: '/forgot-password',
        name: 'ForgotPassword',
        component: ForgotPassword,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
