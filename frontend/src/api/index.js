import baseAPI from "@/api/api.js";


export async function refreshToken() {
    try {
        const response = await baseAPI.post("auth/refresh-token/", localStorage.getItem("refreshToken"))
        const {access, refresh} = response.data
        localStorage.setItem("refreshToken", refresh)
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
        const {access, refresh, username} = response.data
        localStorage.setItem("refreshToken", refresh)
        localStorage.setItem("username", username)
        baseAPI.defaults.headers["Authorization"] = `Bearer ${access}`
        window.dispatchEvent(new Event("auth-changed"))
        return true
    } catch (error) {
        console.error(error)
        return false
    }
}

export async function userLogout() {
    try {
        const data = {
            "refresh": localStorage.getItem("refreshToken")
        }
        const response = await baseAPI.post("auth/logout/", data)
        localStorage.removeItem("refreshToken")
        localStorage.removeItem("username")
        baseAPI.defaults.headers["Authorization"] = ""
        window.dispatchEvent(new Event("auth-changed"))
        return true
    } catch (error) {
        console.error(error)
        return false
    }
}

export const userProfile = (id) => baseAPI.get(`core/users/${id}/`)
