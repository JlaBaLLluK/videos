import baseAPI from "@/api/api.js";
import {ca} from "vuetify/locale";


export async function refreshToken() {
    try {
        const response = await baseAPI.post("auth/refresh-token/", localStorage.getItem("refreshToken"));
        const {access, refresh} = response.data;
        localStorage.setItem("accessToken", access);
        localStorage.setItem("refreshToken", refresh);
        baseAPI.defaults.headers["Authorization"] = `Bearer ${access}`;
    } catch (error) {
        console.log(error);
    }
}

export async function userRegistration(credentials) {
    try {
        const response = await baseAPI.post("core/users/", credentials);
        return {
            data: response.data,
            status: response.status
        }
    } catch (error) {
        return {
            data: error.response.data,
            status: error.response.status
        };
    }
}

export async function userLogin(credentials) {
    try {
        const response = await baseAPI.post("auth/login/", credentials);
        const {access, refresh, username} = response.data;
        localStorage.setItem("accessToken", access);
        localStorage.setItem("refreshToken", refresh);
        baseAPI.defaults.headers["Authorization"] = `Bearer ${access}`;
        await getMe();
        window.dispatchEvent(new Event("user-login"));
        return {
            data: response.data,
            status: response.status
        }
    } catch (error) {
        return {
            data: error.response.data,
            status: error.response.status
        };
    }
}

export async function getMe() {
    const response = await baseAPI.get("core/users/me");
    localStorage.setItem("user", JSON.stringify(response.data));
}

export async function userLogout() {
    try {
        const data = {
            "refresh": localStorage.getItem("refreshToken")
        };
        await baseAPI.post("auth/logout/", data);
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user");
        baseAPI.defaults.headers["Authorization"] = "";
        window.dispatchEvent(new Event("user-logout"));
    } catch (error) {
        console.error(error);
    }
}

export async function getUserData(username) {
    try {
        const response = await baseAPI.get(`core/users/${username}/`);
        return {
            data: response.data,
            status: response.status
        }
    } catch (error) {
        return {
            data: error.response.data,
            status: error.response.status
        };
    }
}
