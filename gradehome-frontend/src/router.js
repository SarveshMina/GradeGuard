import { createRouter, createWebHistory } from 'vue-router';
import AuthLanding from './views/AuthLanding.vue';

const routes = [
    {
        path: '/',
        name: 'AuthLanding',
        component: AuthLanding
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
