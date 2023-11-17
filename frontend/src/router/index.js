import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    { 
        path: '/register', 
        component: () => import('@/components/Registration.vue') 
    },
    { 
        path: '/login', 
        component: () => import('@/components/Login.vue') 
    },
    { 
        path: '/events', 
        component: () => import('@/components/activeCanvas/EventComponent.vue') 
    },
    { 
        path: '/support', 
        component: () => import('@/components/SupportForYou.vue') 
    },
    { 
        path: '/dashboard', 
        component: () => import('@/components/Dashboard.vue') 
    },
    { 
        path: '/', 
        redirect: '/login' 
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router;
