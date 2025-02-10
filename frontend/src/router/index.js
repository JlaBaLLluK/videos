import HomeView from "@/views/HomeView.vue";
import RegisterView from "@/views/RegisterView.vue";
import LoginView from "@/views/LoginView.vue";
import ProfileView from "@/views/ProfileView.vue";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
    },
    {
        path: "/registration",
        name: "registration",
        component: RegisterView,
    },
    {
        path: "/login",
        name: "login",
        component: LoginView,
    },
    {
        path: "/:username",
        name: "profile",
        component: ProfileView,

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