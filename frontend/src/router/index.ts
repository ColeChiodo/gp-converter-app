import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';;

import FileConverter from '../pages/FileConverter/FileConverter.vue';
import About from '../pages/About/About.vue';

const routes: RouteRecordRaw[] = [
    { path: '/', name: 'FileConverter', component: FileConverter },
    { path: '/about', name: 'About', component: About },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
