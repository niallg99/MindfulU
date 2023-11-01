import { createRouter, createWebHistory } from 'vue-router';
import Registration from '@/components/Registration.vue'; // Adjust the path to your Registration.vue file location
import Login from '@/components/Login.vue'; // Adjust the path to your Login.vue file location
import EventComponent from '@/components/activeCanvas/EventComponent.vue'; // Adjust the path if necessary

const routes = [
    { path: '/register', component: Registration },
    { path: '/login', component: Login },
    { path: '/events', component: EventComponent },
    // Redirect to registration page by default
    { path: '/', redirect: '/register' }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router;
