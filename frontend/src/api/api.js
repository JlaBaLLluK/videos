import axios from "axios";

const baseAPI = axios.create({
    baseURL: "http://localhost:8000/api/v1/",
    timeout: 10000,
    headers: {
        "Content-Type": "application/json"
    }
})

export default baseAPI;