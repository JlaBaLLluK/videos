import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("@/views/HomeView.vue"),
    },
    {
        path: "/registration",
        name: "registration",
        component: () => import("@/views/RegistrationView.vue"),
    },
    {
        path: "/login",
        name: "login",
        component: () => import("@/views/LoginView.vue"),
    },
    {
        path: "/:username",
        name: "profile",
        component: () => import("@/views/ProfileView.vue"),

    },
    {
        path: "/logout",
        name: "logout",
        redirect: "/"
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router;