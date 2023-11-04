import { createRouter, createWebHistory } from 'vue-router';
import Registration from '@/components/Registration.vue';
import Login from '@/components/Login.vue';
import EventComponent from '@/components/activeCanvas/EventComponent.vue';

const routes = [
    { path: '/register', component: Registration },
    { path: '/login', component: Login },
    { path: '/events', component: EventComponent },
    { path: '/', redirect: '/login' }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router;
