import HomeView from "@/views/HomeView.vue";
import {createRouter, createWebHistory, createWebHashHistory} from "vue-router";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router;