import baseAPI from "@/api/api.js";


export async function refreshToken() {
    try {
        const response = await baseAPI.post("auth/refresh-token/", localStorage.getItem("refreshToken"));
        const {access, refresh} = response.data;
        localStorage.setItem("refreshToken", refresh);
        baseAPI.defaults.headers["Authorization"] = `Bearer ${access}`;
    } catch (error) {
        console.log(error);
    }
}

export async function userRegistration(credentials) {
    try {
        const response = await baseAPI.post("core/users/", credentials, {
            headers: {
                "Content-Type": "multipart/form-data",
            }
        });
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
        localStorage.setItem("refreshToken", refresh);
        localStorage.setItem("username", username);
        baseAPI.defaults.headers["Authorization"] = `Bearer ${access}`;
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

export async function userLogout() {
    try {
        const data = {
            "refresh": localStorage.getItem("refreshToken")
        };
        await baseAPI.post("auth/logout/", data);
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("username");
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
