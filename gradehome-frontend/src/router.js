// router.js
import { createRouter, createWebHistory } from 'vue-router'
import Landing from './views/Landing.vue'
import Login from './views/Login.vue'
import ForgotPassword from './views/ForgotPassword.vue'
import MobileLanding from './views/MobileLanding.vue'
import Dashboard from './views/Dashboard.vue'
import { Capacitor } from '@capacitor/core'
import UserProfile from "@/components/UserProfile.vue";
import Calendar from "@/components/Calendar.vue";
import SettingsPage from "@/components/SettingsPage.vue"; // Import the Calendar component

// Detect mobile via Capacitor or screen width
const isMobileApp = Capacitor.isNativePlatform() || window.innerWidth <= 768

const routes = [
    {
        path: '/',
        name: 'Home',
        component: isMobileApp ? MobileLanding : Landing,
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
        path: '/profile',
        name: 'Profile',
        component: UserProfile,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/calendar',
        name: 'Calendar',
        component: Calendar,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/forgot-password',
        name: 'ForgotPassword',
        component: ForgotPassword,
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
    },

    {
        path: '/settings',
        name: 'Settings',
        component: SettingsPage,
        meta: {
            requiresAuth: true
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router