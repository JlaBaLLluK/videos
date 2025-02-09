import baseAPI from "@/api/api.js";
import {useRouter} from "vue-router";

export async function refreshToken() {
    try {
        const response = await baseAPI.post("auth/refresh-token/", localStorage.getItem("refreshToken"))
        const {access} = response.data
        localStorage.setItem("accessToken", access)
        baseAPI.defaults.headers["Authorization"] = `Bearer ${access}`
    } catch (error) {
        console.log(error)
    }
}

export function userRegister(credentials) {
    baseAPI.post("core/user/", credentials)
        .then(response => {

        })
        .catch(error => {

        })
}

export async function userLogin(credentials) {
    try {
        const response = await baseAPI.post("auth/login/", credentials)
        const {access, refresh} = response.data
        localStorage.setItem("accessToken", access)
        localStorage.setItem("refreshToken", refresh)
        baseAPI.defaults.headers["Authorization"] = `Bearer ${access}`
    } catch (error) {
        console.error(error)
    }
}

export async function userLogout() {
    try {
        const response = await baseAPI.post("auth/logout/", localStorage.getItem("refreshToken"))
        localStorage.removeItem("accessToken")
        localStorage.removeItem("refreshToken")
        baseAPI.defaults.headers["Authorization"] = ""
    } catch (error) {
        console.error(error)
    }
}

export const userProfile = (id) => baseAPI.get(`core/users/${id}/`)
