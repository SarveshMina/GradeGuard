// router.js
import { createRouter, createWebHistory } from 'vue-router';

// Import your pages:
import Landing from './views/Landing.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';

const routes = [
    {
        path: '/',
        name: 'Landing',
        component: Landing
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
