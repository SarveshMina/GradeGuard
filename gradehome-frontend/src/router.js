// router.js
import { createRouter, createWebHistory } from 'vue-router'
import Landing from './views/Landing.vue'
import Login from './views/Login.vue'
import ForgotPassword from './views/ForgotPassword.vue'
import Dashboard from './views/Dashboard.vue'
import { Capacitor } from '@capacitor/core'
import UserProfile from "@/views/UserProfile.vue";
import Calendar from "@/views/Calendar.vue";
import SettingsPage from "@/views/SettingsPage.vue";
import StudyHub from "@/views/StudyHub.vue";
import UserReviews from './views/UserReviews.vue'
import GradeRadar from './views/GradeRadar.vue'
import UniversityView from './views/UniversityView.vue'
import ModulesList from './views/ModulesList.vue'
import ModuleDetail from './views/ModuleDetail.vue'

// Detect mobile via Capacitor or screen width
// We'll keep this for other potential uses in the app
const isMobileApp = Capacitor.isNativePlatform() || window.innerWidth <= 768

// Get the base URL from the import.meta.env, use the repository name as base
const base = import.meta.env.BASE_URL || '/gradehome.io/'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Landing, // Always use Landing component regardless of device
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
        path: '/study',
        name: 'StudyHub',
        component: StudyHub,
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
        path: '/reset-password',
        name: 'ResetPassword',
        component: Login, // Use the Login component to handle reset password
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
    },

    {
        path: '/graderadar',
        name: 'GradeRadar',
        component: () => import('./views/GradeRadar.vue'),
        meta: { requiresAuth: false }
      },
      {
        path: '/graderadar/university/:university',
        name: 'UniversityView',
        component: () => import('./views/UniversityView.vue'),
        meta: { requiresAuth: false }
      },
      {
        path: '/graderadar/modules/:university/:degree',
        name: 'ModulesList',
        component: () => import('./views/ModulesList.vue'),
        meta: { requiresAuth: false }
      },
      {
        path: '/graderadar/module/:id',
        name: 'ModuleDetail',
        component: () => import('./views/ModuleDetail.vue'),
        meta: { requiresAuth: false }
      },
      {
        path: '/graderadar/user-reviews',
        name: 'UserReviews',
        component: () => import('./views/UserReviews.vue'),
        meta: { requiresAuth: true }
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
    history: createWebHistory(base), // Use the base path here
    routes,
})

export default router