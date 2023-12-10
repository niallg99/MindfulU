import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    { 
        path: '/register',
        name: 'Register', 
        component: () => import('@/components/Registration.vue') 
    },
    { 
        path: '/login', 
        name: 'Login',
        component: () => import('@/components/Login.vue') 
    },
    { 
        path: '/events',
        name: 'Events',
        component: () => import('@/components/activeCanvas/EventComponent.vue') 
    },
    { 
        path: '/support',
        name: 'Support', 
        component: () => import('@/components/SupportForYou.vue') 
    },
    {
        path: '/friends',
        name: 'Friends',
        component: () => import('@/components/Friends.vue')
    },
    { 
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/components/Dashboard.vue') 
    },
    { 
        path: '/admin_dashboard',
        name: 'AdminDashboard',
        component: () => import('@/components/AdminDashboard.vue') 
    },
    { 
        path: '/mood-history', 
        name: 'MoodHistory',
        component: () => import('@/components/MoodHistory.vue') 
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
