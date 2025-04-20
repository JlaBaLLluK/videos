import axios from 'axios';
import router from '@/router/index.js';
import createAuthRefreshInterceptor from 'axios-auth-refresh';
import {errorToast} from '@/plugins/toasts.js';

const baseAPI = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});

async function refreshLogic(failedRequest) {
  if (failedRequest.config.url.includes('/login')) {
    return Promise.reject(failedRequest);
  }
  try {
    const response = await axios.post(
      'http://localhost:8000/api/v1/auth/refresh-token/',
      {refresh: localStorage.getItem('refreshToken')},
    );
    const {access, refresh} = response.data;
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    baseAPI.defaults.headers['Authorization'] = `Bearer ${access}`;
    failedRequest.response.config.headers['Authorization'] = 'Bearer ' + access;
    return Promise.resolve();
  } catch (e) {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    errorToast('Для выполнения этого действия необходимо войти в аккаунт');
    await router.push({name: 'login'});
    return Promise.reject(e);
  }
}

createAuthRefreshInterceptor(baseAPI, refreshLogic);

baseAPI.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 404) {
      router.push({name: 'notFound'});
    }
    else {
      return Promise.reject(error);
    }
  }
);

export default baseAPI;
